# Standard Library
from datetime import datetime, timedelta
from http import HTTPStatus
from typing import List

# Third Party Library
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.event_handler.exceptions import BadRequestError
from aws_lambda_powertools.event_handler.openapi.params import Path, Query
from aws_lambda_powertools.shared.types import Annotated
from controllers.bgl import BGLController
from schemas import errors
from schemas.bgl import BGLCreateRequestSchema, BGLSchema, BGLUpdateRequestSchema

app = APIGatewayRestResolver(debug=True)
router = Router()

controller = BGLController()

logger = Logger("BGLAPI")
tracer = Tracer("BGLAPI")


@tracer.capture_method
@router.get(
    "/",
    tags=["BGL"],
    summary="開発用：全ての血糖値データを取得",
    description="""
## 概要

全ての血糖値データを取得します。

こちらは開発用のエンドポイントです。本番環境で使用されることを想定していません。

## 詳細

全ての血糖値データを取得します。取得したデータは、`BGLSchema`を参照してください。
もし、データが存在しない場合は、空の配列が返されます。

## 仕様

論理削除済みのデータはこれに含まれません。

## 変更履歴

- 2024/5/14: エンドポイントを追加
""",
    response_description="取得したデータの配列",
    operation_id="fetchAllBGLItems",
    responses={
        200: {"description": "全ての血糖値データの取得に成功"},
        400: errors.BAD_REQUEST_ERROR,
        401: errors.UNAUTHORIZED_ERROR,
        500: errors.INTERNAL_SERVER_ERROR,
    },
)
def fetch_all_bgl_items() -> List[BGLSchema]:
    return controller.find_all()  # type: ignore


@tracer.capture_method
@router.get(
    "/<bglId>",
    tags=["BGL"],
    summary="特定の血糖値データを取得",
    description="""
## 概要

idで指定された血糖値データを取得します。

## 詳細

idで指定された血糖値データを取得します。取得したいBGLのデータIDを指定してください。
特定のデータが見つからない場合は、`404 Not Found`が返されます。

特定の血糖値データを取得するためのエンドポイントですが、詳細情報がないので、このエンドポイントはあまり使われることを想定していません。

## 変更履歴

- 2024/5/14: エンドポイントを追加
""",
    response_description="取得したデータ",
    operation_id="fetchSingleBGLItems",
    responses={
        200: {"description": "特定の血糖値データの取得に成功"},
        400: errors.BAD_REQUEST_ERROR,
        401: errors.UNAUTHORIZED_ERROR,
        500: errors.INTERNAL_SERVER_ERROR,
    },
)
def fetch_single_bgl_item(
    bglId: Annotated[
        str,
        Path(
            ...,
            title="BGLデータID",
            description="取得したいBGLのデータID",
            example="e7b45a9810317095d7ee6748af941d2",
        ),
    ]
) -> BGLSchema:
    return controller.find_one(bglId)


@tracer.capture_method
@router.post(
    "/",
    tags=["BGL"],
    summary="新規血糖値データを登録",
    description="""
## 概要

血糖値データを新規に登録します。

## 詳細

血糖値データを新規に登録します。登録するデータは、`BGLCreateRequestSchema`を参照してください。
データの登録に成功した場合は、登録したデータが返されます。

## 変更履歴

- 2024/5/14: エンドポイントを追加
""",
    response_description="作成されたデータ",
    operation_id="createBGLItem",
    responses={
        201: {"description": "新規の血糖値データの作成に成功"},
        400: errors.BAD_REQUEST_ERROR,
        401: errors.UNAUTHORIZED_ERROR,
        500: errors.INTERNAL_SERVER_ERROR,
    },
)
def create_bgl_item(item: BGLCreateRequestSchema) -> BGLSchema:
    return controller.create_one(item), HTTPStatus.CREATED


@tracer.capture_method
@router.put(
    "/<bglId>",
    tags=["BGL"],
    summary="特定の血糖値データを更新",
    description="""
## 概要

idで指定された血糖値データを更新します。

## 詳細

idで指定された血糖値データを更新します。更新するデータは、`BGLUpdateRequestSchema`を参照してください。

## 仕様

変更に関して、`dynamodb`の仕様により、`range key`の変更ができない仕様になります。
そのため、更新は実質的に削除と新規作成の組み合わせとなります。
よって、**データのIDが変更されることに注意**してください。

## 変更履歴

- 2024/5/14: エンドポイントを追加
""",
    response_description="更新されたデータ",
    operation_id="updateBGLItem",
    responses={
        200: {"description": "血糖値データの更新に成功"},
        400: errors.BAD_REQUEST_ERROR,
        401: errors.UNAUTHORIZED_ERROR,
        500: errors.INTERNAL_SERVER_ERROR,
    },
)
def update_bgl_item(
    bglId: Annotated[
        str,
        Path(
            ...,
            title="BGLデータID",
            description="更新したいBGLのデータID",
            example="e7b45a9810317095d7ee6748af941d2",
        ),
    ],
    item: BGLUpdateRequestSchema,
) -> BGLSchema:
    return controller.update_one(bglId, item)


@tracer.capture_method
@router.delete(
    "/<bglId>",
    tags=["BGL"],
    summary="特定の血糖値データを削除",
    description="""
## 概要

IDで指定された血糖値データを論理削除します。

## 詳細

IDで指定された血糖値データを論理削除します。削除されたデータは、`deleted`フラグが`True`になります。
論理削除なので、データは実際には削除されませんが、取得系のエンドポイントで取得されることはなくなります。

もし、データを復元したい場合は、ユースケースにもよりますが、新たにエンドポイントを追加することになるので髙橋までご連絡ください。

## 変更履歴

- 2024/5/14: エンドポイントを追加
""",
    response_description="削除したデータ",
    operation_id="deleteBGLItem",
    responses={
        200: {"description": "データの論理削除に成功"},
        400: errors.BAD_REQUEST_ERROR,
        401: errors.UNAUTHORIZED_ERROR,
        500: errors.INTERNAL_SERVER_ERROR,
    },
)
def delete_bgl_item(
    bglId: Annotated[
        str,
        Path(
            ...,
            title="BGLデータID",
            description="削除したいBGLのデータID",
            example="e7b45a9810317095d7ee6748af941d2",
        ),
    ],
) -> BGLSchema:
    return controller.delete_one(bglId)


@tracer.capture_method
@router.get(
    "/query",
    tags=["BGL"],
    summary="クエリパラメータを使ったデータの取得",
    description="""
## 概要

クエリパラメータを使って、特定のユーザーの期間内における血糖値データを取得します。

## 詳細

クエリパラメータを使って、特定のユーザーの期間内における血糖値データを取得します。

## 仕様

取得できるデータは、指定されたユーザーIDに紐づくデータのみです。
また、指定された期間内のデータのみ取得されます。
指定された期間は、開始日と終了日の両方が含まれます。

## 変更履歴

- 2024/5/14: エンドポイントを追加
""",
    response_description="取得したデータの配列",
    operation_id="queryBGLItems",
    responses={
        200: {"description": "指定されたデータの取得に成功"},
        400: errors.BAD_REQUEST_ERROR,
        401: errors.UNAUTHORIZED_ERROR,
        500: errors.INTERNAL_SERVER_ERROR,
    },
)
def fetch_bgl_items_by_user_id(
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
) -> List[BGLSchema]:
    try:
        __from = datetime.strptime(_from, "%Y%m%d")
        __to = datetime.strptime(_to, "%Y%m%d")
        if _from > _to:
            raise BadRequestError("Invalid date range. Start date should be less than end date")
    except ValueError:
        raise BadRequestError("Invalid date format. Please use YYYYMMDD format")
    return controller.find_many_by_user_id(userId, __from, __to)  # type: ignore
