# Third Party Library
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.openapi.models import Contact, Server
from aws_lambda_powertools.utilities.typing import LambdaContext
from config.api import STAGE
from database.base import BGLModel, Hba1cModel
from middlewares.common import handler_middleware
from pydantic import BaseModel, Field
from pydantic.networks import AnyUrl
from routes import bgl, hba1c

logger = Logger()

if STAGE == "local" or STAGE == "dev":
    if not BGLModel.exists():
        logger.info("Creating BGLModel table")
        BGLModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    if not Hba1cModel.exists():
        logger.info("Creating Hba1cModel table")
        Hba1cModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)

local_server = Server(
    url="http://localhost:3333", description="Local Development Server", variables=None
)
dev_server = Server(
    url="https://5v3zfa18l1.execute-api.ap-northeast-1.amazonaws.com/dev",
    description="Development Server",
    variables=None,
)

servers = []
if STAGE == "local":
    servers.append(local_server)
if STAGE == "dev":
    servers.append(dev_server)

app = APIGatewayRestResolver(enable_validation=True)
app.enable_swagger(
    path="/swagger",
    title="Glico SUNAO 血糖値管理アプリAPI仕様書",
    summary="Glico SUNAO 血糖値管理アプリケーションのバックエンドAPIの仕様書です。",
    description="""
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


class HealthCheckSchema(BaseModel):
    status: str = Field(..., description="Health Check Status", example="ok")  # type: ignore


@app.get(
    "/healthcheck",
    cors=True,
    summary="Health Check",
    description="Check the health of the application.",
    response_description="Health Check",
    tags=["default"],
    operation_id="healthcheck",
)
def health_check() -> HealthCheckSchema:
    return HealthCheckSchema(**{"status": "ok"})


@handler_middleware
@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: dict, context: LambdaContext) -> dict[str, str | int]:
    return app.resolve(event, context)
