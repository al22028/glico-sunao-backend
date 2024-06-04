# Standard Library
from typing import List

# Third Party Library
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import Router
from controllers.user import UserController
from schemas import errors
from schemas.user import UserCreateRequestSchema, UserSchema

app = APIGatewayRestResolver(debug=True)
router = Router()

controller = UserController()

logger = Logger("UserAPI")
tracer = Tracer("UserAPI")


@router.get(
    "/",
    tags=["User"],
    summary="全てのユーザーデータを取得",
    description="""
## 概要

全てのユーザーデータを取得します。

## 変更履歴

- 2024/6/3: エンドポイントを追加
""",
    response_description="全てのユーザーデータの取得に成功",
    operation_id="fetchAllUserData",
    responses={
        200: {"description": "全てのユーザーデータの取得に成功"},
        400: errors.BAD_REQUEST_ERROR,
        401: errors.UNAUTHORIZED_ERROR,
        500: errors.INTERNAL_SERVER_ERROR,
    },
)
def find_all() -> List[UserSchema]:
    return controller.find_all()  # type: ignore


@router.post(
    "/",
    tags=["User"],
    summary="ユーザーデータを登録",
    description="""
## 概要

ユーザーデータを登録します。

## 変更履歴

- 2024/6/4: エンドポイントを追加
""",
    response_description="ユーザーデータの登録に成功",
    operation_id="createUserData",
    responses={
        200: {"description": "ユーザーデータの登録に成功"},
        400: errors.BAD_REQUEST_ERROR,
        401: errors.UNAUTHORIZED_ERROR,
        500: errors.INTERNAL_SERVER_ERROR,
    },
)
def create_one(data: UserCreateRequestSchema) -> UserSchema:
    return controller.create_one(data)
