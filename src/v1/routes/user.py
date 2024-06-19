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
    summary="開発用：全てのユーザーデータを取得",
    description="""
## 概要

開発用に全てのユーザーデータを取得します。
このエンドポイントは開発用途のみで使用してください。

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


@router.get(
    "/<userId>",
    tags=["User"],
    summary="IDを指定してユーザーデータを取得",
    description="""
## 概要

IDを指定してユーザーデータを取得します。

## 変更履歴

- 2024/6/4: エンドポイントを追加
""",
    response_description="ユーザーデータの取得に成功",
    operation_id="fetchUserDataById",
    responses={
        200: {"description": "ユーザーデータの取得に成功"},
        400: errors.BAD_REQUEST_ERROR,
        401: errors.UNAUTHORIZED_ERROR,
        404: errors.NOT_FOUND_ERROR,
        500: errors.INTERNAL_SERVER_ERROR,
    },
)
def find_one(userId: str) -> UserSchema:
    return controller.find_one(userId)


@router.post(
    "/",
    tags=["User"],
    summary="ユーザーデータを登録",
    description="""
## 概要

ユーザーデータを登録します。

## 詳細

ユーザーが規約に同意したかどうかを表す`termAgreed`を受け取り、ユーザーデータを登録します。

## 変更履歴

- 2024/6/4: エンドポイントを追加
""",
    response_description="ユーザーデータの登録に成功",
    operation_id="createUserData",
    responses={
        201: {"description": "ユーザーデータの登録に成功"},
        400: errors.BAD_REQUEST_ERROR,
        401: errors.UNAUTHORIZED_ERROR,
        500: errors.INTERNAL_SERVER_ERROR,
    },
)
def create_one(data: UserCreateRequestSchema) -> UserSchema:
    return controller.create_one(data)


@router.patch(
    "/<userId>",
    tags=["User"],
    summary="ユーザーを規約同意済み状態に更新",
    description="""
## 概要

ユーザーを規約同意済み状態に更新します。

## 詳細

`termAgreedAt`の値を現在時刻に更新します。

## 変更履歴

- 2024/6/4: エンドポイントを追加
""",
    response_description="ユーザーを規約同意済み状態に更新",
    operation_id="updateUserTermStatus",
    responses={
        200: {"description": "ユーザーを規約同意済み状態に更新"},
        400: errors.BAD_REQUEST_ERROR,
        401: errors.UNAUTHORIZED_ERROR,
        404: errors.NOT_FOUND_ERROR,
        500: errors.INTERNAL_SERVER_ERROR,
    },
)
def update_term_agreed_at(userId: str) -> UserSchema:
    return controller.update_term_agreed_at(userId)


@router.delete(
    "/<userId>",
    tags=["User"],
    summary="ユーザーを論理削除",
    description="""
## 概要

ユーザーを論理削除します。

## 変更履歴

- 2024/6/19: エンドポイントを追加

""",
    response_description="ユーザーの論理削除に成功",
    operation_id="deleteUserData",
    responses={
        200: {"description": "ユーザーの論理削除に成功"},
        400: errors.BAD_REQUEST_ERROR,
        401: errors.UNAUTHORIZED_ERROR,
        404: errors.NOT_FOUND_ERROR,
        500: errors.INTERNAL_SERVER_ERROR,
    },
)
def delete_single_user(userId: str) -> UserSchema:
    return controller.delete_single_user(userId)
