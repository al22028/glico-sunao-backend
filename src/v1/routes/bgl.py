# Standard Library
from typing import List

# Third Party Library
# from aws_lambda_powertools import Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import Router
from models.bgl import BGLModelORM
from schemas.bgl import BGLCreateRequestSchema, BGLSchema

app = APIGatewayRestResolver(debug=True)
router = Router()

bgl = BGLModelORM()


@router.get(
    "/",
    tags=["BGL"],
    summary="全ての血糖値データを取得",
    description="全ての血糖値データを取得します。",
    response_description="AllBGLItems",
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
    response_description="SingleBGLItem",
    operation_id="fetchSingleBGLItems",
)
def fetch_single_bgl_item(bglId: str) -> BGLSchema:
    data = bgl.find_one(bglId)
    return data.serializer()


@router.post(
    "/",
    tags=["BGL"],
    summary="血糖値データを作成",
    description="血糖値データを新規作成します。",
    response_description="Created BGL Item",
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
    response_description="Updated BGL Item",
    operation_id="updateBGLItem",
)
def update_bgl_item(bglId: str, item: BGLCreateRequestSchema) -> BGLSchema:
    data = bgl.update_one(bglId, item)
    return data.serializer()


@router.delete(
    "/<bglId>",
    tags=["BGL"],
    summary="特定の血糖値データを削除",
    description="idで指定された血糖値データを削除します。",
    response_description="Deleted BGL Item",
    operation_id="deleteBGLItem",
)
def delete_bgl_item(bglId: str) -> BGLSchema:
    data = bgl.delete_one(bglId)
    return data.serializer()
