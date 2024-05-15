# Standard Library
from datetime import datetime, timedelta
from http import HTTPStatus
from typing import List

# Third Party Library
from aws_lambda_powertools import Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.event_handler.exceptions import BadRequestError
from aws_lambda_powertools.event_handler.openapi.params import Path, Query
from aws_lambda_powertools.shared.types import Annotated
from controllers.hba1c import Hba1cController
from schemas import errors
from schemas.hba1c import Hba1cCreateRequestSchema, Hba1cSchema, Hba1cUpdateRequestSchema

app = APIGatewayRestResolver(debug=True)
router = Router()

tracer = Tracer("Hba1cAPI")

controller = Hba1cController()


@tracer.capture_method
@router.get(
    "/",
    tags=["Hba1c"],
    summary="開発用：全てのHba1cデータを取得",
    description="""
## 概要

全てのHba1cデータを取得します。

こちらは開発用のエンドポイントです。本番環境で使用されることを想定していません。

## 詳細

全てのHba1cデータを取得します。取得したデータは、`Hba1cSchema`を参照してください。
もし、データが存在しない場合は、空の配列が返されます。

## 仕様

<strike>論理削除済みのデータはこれに含まれません。</strike>

## 変更履歴

- 2024/5/14: エンドポイントを追加
- 2024/5/15: 論理削除済みのデータを含めるように仕様変更
""",
    response_description="取得したデータの配列",
    operation_id="fetchAllHba1cItems",
    responses={
        200: {"description": "全てのHba1cデータの取得に成功"},
        400: errors.BAD_REQUEST_ERROR,
        401: errors.UNAUTHORIZED_ERROR,
        500: errors.INTERNAL_SERVER_ERROR,
    },
)
def fetch_all_Hba1c_items() -> List[Hba1cSchema]:
    return controller.find_all()  # type: ignore


@tracer.capture_method
@router.get(
    "/<Hba1cId>",
    tags=["Hba1c"],
    summary="特定のHba1cデータを取得",
    description="""
## 概要

idで指定されたHba1cデータを取得します。

## 詳細

idで指定されたHba1cデータを取得します。取得したいHba1cのデータIDを指定してください。
指定されたデータが見つからない場合は、`404 Not Found`が返されます。

特定のHba1cデータを取得するためのエンドポイントですが、詳細情報がないので、このエンドポイントはあまり使われることを想定していません。

## 変更履歴

- 2024/5/14: エンドポイントを追加
""",
    response_description="取得したデータ",
    operation_id="fetchSingleHba1cItems",
    responses={
        200: {"description": "特定のHba1cデータの取得に成功"},
        400: errors.BAD_REQUEST_ERROR,
        401: errors.UNAUTHORIZED_ERROR,
        500: errors.INTERNAL_SERVER_ERROR,
    },
)
def fetch_single_Hba1c_item(
    Hba1cId: Annotated[
        str,
        Path(
            ...,
            title="Hba1cデータID",
            description="取得したいHba1cのデータID",
            example="e7b45a9810317095d7ee6748af941d2",
        ),
    ]
) -> Hba1cSchema:
    return controller.find_one(Hba1cId)


@tracer.capture_method
@router.post(
    "/",
    tags=["Hba1c"],
    summary="新規Hba1cデータを登録",
    description="""
## 概要

Hba1cデータを新規に登録します。

## 詳細

Hba1cデータを新規に登録します。登録するデータは、`Hba1cCreateRequestSchema`を参照してください。
データの登録に成功した場合は、登録したデータが返されます。

## 変更履歴

- 2024/5/14: エンドポイントを追加
""",
    response_description="作成されたデータ",
    operation_id="createHba1cItem",
    responses={
        201: {"description": "新規Hba1cデータの登録に成功"},
        400: errors.BAD_REQUEST_ERROR,
        401: errors.UNAUTHORIZED_ERROR,
        500: errors.INTERNAL_SERVER_ERROR,
    },
)
def create_Hba1c_item(item: Hba1cCreateRequestSchema) -> Hba1cSchema:
    return controller.create_one(item), HTTPStatus.CREATED


@tracer.capture_method
@router.put(
    "/<Hba1cId>",
    tags=["Hba1c"],
    summary="特定のHba1cデータを更新",
    description="""
## 概要

idで指定されたHba1cデータを更新します。

## 詳細

idで指定されたHba1cデータを更新します。更新するデータは、`Hba1cUpdateRequestSchema`を参照してください。

## 仕様

変更に関して、`dynamodb`の仕様により、`range key`の変更ができない仕様になります。
そのため、更新は実質的に削除と新規作成の組み合わせとなります。
よって、**データのIDが変更されることに注意**してください。

## 変更履歴

- 2024/5/14: エンドポイントを追加
""",
    response_description="更新されたデータ",
    operation_id="updateHba1cItem",
    responses={
        200: {"description": "特定のHba1cデータの更新に成功"},
        400: errors.BAD_REQUEST_ERROR,
        401: errors.UNAUTHORIZED_ERROR,
        500: errors.INTERNAL_SERVER_ERROR,
    },
)
def update_Hba1c_item(
    Hba1cId: Annotated[
        str,
        Path(
            ...,
            title="Hba1cデータID",
            description="更新したいHba1cのデータID",
            example="e7b45a9810317095d7ee6748af941d2",
        ),
    ],
    item: Hba1cUpdateRequestSchema,
) -> Hba1cSchema:
    return controller.update_one(Hba1cId, item)


@tracer.capture_method
@router.delete(
    "/<Hba1cId>",
    tags=["Hba1c"],
    summary="特定のHba1cデータを論理削除",
    description="""
## 概要

IDで指定されたHba1cデータを論理削除します。

## 詳細

IDで指定されたHba1cデータを論理削除します。論理削除されたデータは、`deleted`フラグが`True`になります。
論理削除なので、データは実際には削除されませんが、取得系のエンドポイントで取得されることはなくなります。

もし、データを復元したい場合は、ユースケースにもよりますが、新たにエンドポイントを追加することになるので髙橋までご連絡ください。

## 変更履歴

- 2024/5/14: エンドポイントを追加
""",
    response_description="削除したデータ",
    operation_id="deleteHba1cItem",
    responses={
        200: {"description": "特定のHba1cデータの論理削除に成功"},
        400: errors.BAD_REQUEST_ERROR,
        401: errors.UNAUTHORIZED_ERROR,
        500: errors.INTERNAL_SERVER_ERROR,
    },
)
def delete_Hba1c_item(
    Hba1cId: Annotated[
        str,
        Path(
            ...,
            title="Hba1cデータID",
            description="削除したいHba1cのデータID",
            example="e7b45a9810317095d7ee6748af941d2",
        ),
    ],
) -> Hba1cSchema:
    return controller.delete_one(Hba1cId)


@tracer.capture_method
@router.get(
    "/query",
    tags=["Hba1c"],
    summary="クエリパラメータを使ったデータの取得",
    description="""
## 概要

クエリパラメータを使って、特定のユーザーの期間内におけるHba1cデータを取得します。

## 詳細

クエリパラメータを使って、特定のユーザーの期間内におけるHba1cデータを取得します。

## 仕様

取得できるデータは、指定されたユーザーIDに紐づくデータのみです。
また、指定された期間内のデータのみ取得されます。
指定された期間は、開始日と終了日の両方が含まれます。

## 変更履歴

- 2024/5/14: エンドポイントを追加
""",
    response_description="取得したデータの配列",
    operation_id="queryHba1cItems",
    responses={
        200: {"description": "指定されたデータの取得に成功"},
        400: errors.BAD_REQUEST_ERROR,
        401: errors.UNAUTHORIZED_ERROR,
        500: errors.INTERNAL_SERVER_ERROR,
    },
)
def fetch_Hba1c_items_by_user_id(
    userId: Annotated[
        str,
        Query(
            ...,
            title="ユーザーID",
            description="取得したいユーザーのID",
            example="asds45a98103195d7ee6748af941d2",
        ),
    ],
    _from: Annotated[
        str,
        Query(
            ...,
            alias="from",
            title="範囲開始日",
            description="取得したいデータの範囲開始日",
            example=(datetime.now() - timedelta(days=7)).strftime("%Y%m%d"),
        ),
    ],
    _to: Annotated[
        str,
        Query(
            ...,
            alias="to",
            title="範囲終了日",
            description="取得したいデータの範囲終了日",
            example=datetime.now().strftime("%Y%m%d"),
        ),
    ],
) -> List[Hba1cSchema]:
    try:
        __from = datetime.strptime(_from, "%Y%m%d")
        __to = datetime.strptime(_to, "%Y%m%d")
        if _from > _to:
            raise BadRequestError("Invalid date range. Start date should be less than end date")
    except ValueError:
        raise BadRequestError("Invalid date format. Please use YYYYMMDD format")
    return controller.find_many_by_user_id(userId, __from, __to)  # type: ignore
