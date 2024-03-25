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
from database.base import Hba1cModel
from models.hba1c import Hba1cModelORM
from schemas.hba1c import Hba1cCreateRequestSchema, Hba1cSchema

app = APIGatewayRestResolver(debug=True)
router = Router()

Hba1c = Hba1cModelORM()


@router.get(
    "/",
    tags=["Hba1c"],
    summary="全てのHba1cデータを取得",
    description="全てのHba1cデータを取得します。",
    response_description="取得したデータの配列",
    operation_id="fetchAllHba1cItems",
)
def fetch_all_Hba1c_items() -> List[Hba1cSchema]:
    items = Hba1c.find_all()
    return [item.serializer() for item in items]


@router.get(
    "/<Hba1cId>",
    tags=["Hba1c"],
    summary="特定のHba1cデータを取得",
    description="idで指定されたHba1cデータを取得します。",
    response_description="取得したデータ",
    operation_id="fetchSingleHba1cItems",
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
    data = Hba1c.find_one(Hba1cId)
    return data.serializer()


@router.post(
    "/",
    tags=["Hba1c"],
    summary="Hba1cデータを作成",
    description="Hba1cデータを新規作成します。",
    response_description="作成されたデータ",
    operation_id="createHba1cItem",
)
def create_Hba1c_item(item: Hba1cCreateRequestSchema) -> Hba1cSchema:
    data = Hba1c.create_one(item)
    return data.serializer()


@router.put(
    "/<Hba1cId>",
    tags=["Hba1c"],
    summary="特定のHba1cデータを更新",
    description="idで指定されたHba1cデータを更新します。",
    response_description="更新されたデータ",
    operation_id="updateHba1cItem",
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
    item: Hba1cCreateRequestSchema,
) -> Hba1cSchema:
    data = Hba1c.update_one(Hba1cId, item)
    return data.serializer()


@router.delete(
    "/<Hba1cId>",
    tags=["Hba1c"],
    summary="特定のHba1cデータを削除",
    description="idで指定されたHba1cデータを削除します。",
    response_description="削除したデータ",
    operation_id="deleteHba1cItem",
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
    data = Hba1c.delete_one(Hba1cId)
    return data.serializer()


@router.get(
    "/query",
    tags=["Hba1c"],
    summary="クエリパラメータを使ったデータの取得",
    response_description="取得したデータの配列",
    operation_id="queryHba1cItems",
)
def fetch_Hba1c_items_by_user_id(
    user_id: Annotated[
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
) -> List[Hba1cSchema]:
    try:
        __from = datetime.strptime(_from, "%Y%m%d")
        __to = datetime.strptime(_to, "%Y%m%d")
        if _from > _to:
            raise BadRequestError("Invalid date range. Start date should be less than end date")
    except ValueError:
        raise BadRequestError("Invalid date format. Please use YYYYMMDD format")
    items: List[Hba1cModel] = Hba1c.find_many_by_user_id(user_id, __from, __to)
    return [item.serializer() for item in items]
