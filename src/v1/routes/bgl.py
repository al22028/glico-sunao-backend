# Standard Library
from datetime import datetime
from typing import List

# Third Party Library
# from aws_lambda_powertools import Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.event_handler.exceptions import BadRequestError
from aws_lambda_powertools.event_handler.openapi.params import Path, Query
from aws_lambda_powertools.shared.types import Annotated
from database.base import BGLModel
from models.bgl import BGLModelORM
from schemas.bgl import BGLCreateRequestSchema, BGLSchema, BGLUpdateRequestSchema

app = APIGatewayRestResolver(debug=True)
router = Router()

bgl = BGLModelORM()


@router.get(
    "/",
    tags=["BGL"],
    summary="全ての血糖値データを取得",
    description="全ての血糖値データを取得します。",
    response_description="取得したデータの配列",
    operation_id="fetchAllBGLItems",
)
def fetch_all_bgl_items() -> List[BGLSchema]:
    items = bgl.find_all()
    return [item.serializer() for item in items]


@router.get(
    "/<bglId>",
    tags=["BGL"],
    summary="特定の血糖値データを取得",
    description="idで指定された血糖値データを取得します。",
    response_description="取得したデータ",
    operation_id="fetchSingleBGLItems",
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
    data = bgl.find_one(bglId)
    return data.serializer()


@router.post(
    "/",
    tags=["BGL"],
    summary="血糖値データを作成",
    description="血糖値データを新規作成します。",
    response_description="作成されたデータ",
    operation_id="createBGLItem",
)
def create_bgl_item(item: BGLCreateRequestSchema) -> BGLSchema:
    data = bgl.create_one(item)
    return data.serializer()


@router.put(
    "/<bglId>",
    tags=["BGL"],
    summary="特定の血糖値データを更新",
    description="idで指定された血糖値データを更新します。",
    response_description="更新されたデータ",
    operation_id="updateBGLItem",
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
    data = bgl.update_one(bglId, item)
    return data.serializer()


@router.delete(
    "/<bglId>",
    tags=["BGL"],
    summary="特定の血糖値データを削除",
    description="idで指定された血糖値データを削除します。",
    response_description="削除したデータ",
    operation_id="deleteBGLItem",
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
    data = bgl.delete_one(bglId)
    return data.serializer()


@router.get(
    "/query",
    tags=["BGL"],
    summary="クエリパラメータを使ったデータの取得",
    response_description="取得したデータの配列",
    operation_id="queryBGLItems",
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
            example="20240317",
        ),
    ],
    _to: Annotated[
        str,
        Query(
            ...,
            alias="to",
            title="範囲終了日",
            description="取得したいデータの範囲終了日",
            example="20240319",
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
    items: List[BGLModel] = bgl.find_many_by_user_id(userId, __from, __to)
    return [item.serializer() for item in items]
