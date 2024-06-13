# Standard Library
from datetime import datetime
from typing import List

# Third Party Library
from aws.s3_client import S3Client
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.openapi.models import Contact, Server
from aws_lambda_powertools.utilities.typing import LambdaContext
from config.api import API_VERSION_HASH, APP_API_BASE_URL, STAGE
from database.base import BGLModel, Hba1cModel, UserModel
from middlewares.common import cors_middleware, handler_middleware, log_request_response
from pydantic import BaseModel, Field
from pydantic.networks import AnyUrl
from routes import bgl, hba1c, user
from schemas.log_schema import LogSchema

logger = Logger("ApplicationHandler")
tracer = Tracer("ApplicationHandler")

s3_client = S3Client()

if STAGE == "local" or STAGE == "dev":
    if not BGLModel.exists():
        logger.info("Creating BGLModel table")
        BGLModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    if not Hba1cModel.exists():
        logger.info("Creating Hba1cModel table")
        Hba1cModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    if not UserModel.exists():
        logger.info("Creating UserModel table")
        UserModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)

local_server = Server(
    url="http://localhost:3333", description="Local Development Server", variables=None
)
dev_server = Server(
    url=APP_API_BASE_URL,
    description="Development Server",
    variables=None,
)

servers: List[Server] = []
if STAGE == "local":
    servers.append(local_server)
if STAGE == "dev":
    servers.append(dev_server)


app = APIGatewayRestResolver(enable_validation=True)
# ミドルウェアの登録
app.use(middlewares=[log_request_response, cors_middleware])

app.enable_swagger(
    path="/swagger",
    title="Glico SUNAO 血糖値管理アプリAPI仕様書",
    version=API_VERSION_HASH,
    summary="Glico SUNAO 血糖値管理アプリケーションのバックエンドAPIの仕様書です。",
    description=f"""
![グリコロゴ](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSOeSsMRCo0cMhs1bP4fb-1D45pii-LkGZcpg&s)
![SUNAOロゴ](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRcdtPpgEs9hfDcMxq_WJEZk7pAkHVkYtx_EA&s)
![つばさ株式会社ロゴ](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTUF74Gsbwzr3N9Rsjok_lGoYgAa_r8CSZE0lV_HqlAAw&s)

## 概要

Glico SUNAO 血糖値管理アプリAPI仕様書。血糖値管理アプリケーションのバックエンドAPIを提供します。

## 仕様書について

仕様書（ドキュメント）の生成は、AWS Lambda Powertools の OpenAPI version 3.1.0 仕様書を使用し、半自動で生成されています。
もし、APIについての質問や提案があれば、髙橋までご連絡ください。

## リクエストとレスポンスのフォーマット

リクエストとレスポンスのフォーマットは、JSON 形式で提供されます。
リクエストに関しての詳細は、各エンドポイントの仕様を参照してください。

## APIのバージョン情報

APIのバージョンは、`{API_VERSION_HASH}` です。このバージョンは、ローカルからデプロイされた場合`latest` になります。
GitHub Actions によるCI/CD でデプロイされた場合は、コミットハッシュが付与されたバージョンになります。このバージョン情報は、ヘルスチェックエンドポイントで確認することもできます。

    """,
    contact=Contact(
        name="Takahashi Katsuyuki",
        email="takahashi.k@world-wing.com",
        url=AnyUrl("https://github.com/kkml4220"),
    ),
    servers=servers,
)

app.include_router(router=bgl.router, prefix="/bgl")
app.include_router(router=hba1c.router, prefix="/hba1c")
app.include_router(router=user.router, prefix="/user")


class HealthCheckSchema(BaseModel):
    status: str = Field(
        ...,
        title="ヘルスチェックステータス",
        description="""
Health Check Status
""",
        example="ok",  # type: ignore
    )
    version: str = Field(
        ...,
        title="APIのバージョン情報",
        description="""
## 概要

APIのバージョン情報を提供します。

## 詳細

APIのバージョン情報を提供します。バージョン情報は、環境変数 `API_VERSION_HASH` に設定されている値を返します。
ローカルからデプロイされた場合は、`latest` が返されます。もし、`GitHub Actions` でデプロイされた場合は、コミットハッシュの値を含む文字列が返されます。
""",
        example="latest",  # type: ignore
    )


@app.get(
    "/healthcheck",
    cors=True,
    summary="Health Check",
    description="""
## 概要

サーバーの稼働状況とAPIのバージョン情報を取得します

## 詳細

基本的には常に Status Code 200: で`ok` が返却されます。
それ以外の場合は、サーバーに問題が発生している可能性がありますのでお手数ですが、髙橋までご連絡ください。

APIのバージョンに関しては、ローカルからデプロイされた場合`latest` になります。
GitHub Actions によるCI/CD でデプロイされた場合は、コミットハッシュが付与されたバージョンになります。

## 変更履歴
- 2024/05/14: エンドポイントを追加
- 2024/05/15: バージョン情報を追加
""",
    response_description="Health Check",
    tags=["default"],
    operation_id="healthcheck",
)
def health_check() -> HealthCheckSchema:
    return HealthCheckSchema(**{"status": "ok", "version": API_VERSION_HASH})


@app.post(
    "/logs/<userId>/qr",
    cors=True,
    summary="ログを取得",
    operation_id="saveLogsToS3",
    description="""QRコードのログをS3に保存するエンドポイント""",
)
def save_logs_to_s3(userId: str, log_data: LogSchema) -> dict[str, str]:
    now = datetime.now().isoformat()
    s3_client.put_object(key=f"logs/{userId}/{now}.json", body=log_data.model_dump_json().encode())
    return {"message": f"Logs saved to S3 by {userId}"}


@handler_middleware
@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: dict, context: LambdaContext) -> dict[str, str | int]:
    return app.resolve(event, context)
