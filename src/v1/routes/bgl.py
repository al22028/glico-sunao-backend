# Standard Library
from typing import List

# Third Party Library
from aws_lambda_powertools import Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import Router
from models.bgl import BGLModelORM
from schemas.bgl import BGLSchema

app = APIGatewayRestResolver(debug=True)
router = Router()
tracer = Tracer()

bgl = BGLModelORM()


@router.get(
    "/",
    tags=["BGL"],
    summary="全ての血糖値データを取得",
    description="ての血糖値データを取得します。",
    response_description="AllBGLItems",
    operation_id="fetchAllBGLItems",
)
def fetch_all_bgl_items() -> List[BGLSchema]:
    items = bgl.find_all()
    return [BGLSchema(**item) for item in items]
