# Standard Library
from datetime import datetime, timedelta
from typing import List

# Third Party Library
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import Router
from controllers.bgl_and_hba1c import BGLAndHba1cController
from schemas.bgl import BGLSchema
from aws_lambda_powertools.shared.types import Annotated
from aws_lambda_powertools.event_handler.openapi.params import Query
from aws_lambda_powertools.event_handler.exceptions import BadRequestError


app = APIGatewayRestResolver(debug=True)
router = Router()

controller = BGLAndHba1cController()

logger = Logger("BGLAndHba1cAPI")
tracer = Tracer("BGLAndHba1cAPI")

@router.get(
    "/query",
    tags=["BGLAndHba1c"],
)
def combine_bgl_and_hba1c_list(
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
        if _from > _to:
            raise BadRequestError("Invalid date range. Start date should be less than end date")
    except ValueError:
        raise BadRequestError("Invalid date format. Please use YYYYMMDD format")
    return controller.combine_bgl_and_hba1c_list(userId, _from, _to) # type: ignore
