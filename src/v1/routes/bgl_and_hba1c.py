# Standard Library
from datetime import datetime, timedelta
from typing import List

# Third Party Library
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.event_handler.exceptions import BadRequestError
from aws_lambda_powertools.event_handler.openapi.params import Query
from aws_lambda_powertools.shared.types import Annotated
from controllers.bgl_and_hba1c import BGLAndHba1cController
from schemas import errors
from schemas.bgl_and_hba1c import BGLAndHba1cSchema

app = APIGatewayRestResolver(debug=True)
router = Router()

controller = BGLAndHba1cController()

logger = Logger("BGLAndHba1cAPI")
tracer = Tracer("BGLAndHba1cAPI")


@router.get(
    "/query",
    tags=["BGLAndHba1c"],
    summary="クエリパラメータを使ったBGLとHbA1cデータの取得",
    description="""
## 概要

クエリパラメータを使って、特定のユーザーの期間内における血糖値とHbA1cデータを取得します。

## 詳細
データは日時をキーとして昇順にソートされています。

## 仕様
取得できるデータは、指定されたユーザーIDに紐づくデータのみです。
また、指定された期間内のデータのみ取得されます。
指定された期間は、開始日と終了日の両方が含まれます。

## 変更履歴

- 2024/6/13: エンドポイントを追加
""",
    response_description="取得したデータの配列",
    operation_id="queryBGLAndHba1cItems",
    responses={
        200: {"description": "指定されたデータの取得に成功"},
        400: errors.BAD_REQUEST_ERROR,
        401: errors.UNAUTHORIZED_ERROR,
        500: errors.INTERNAL_SERVER_ERROR,
    },
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
) -> List[BGLAndHba1cSchema]:
    try:
        if _from > _to:
            raise BadRequestError("Invalid date range. Start date should be less than end date")
    except ValueError:
        raise BadRequestError("Invalid date format. Please use YYYYMMDD format")
    return controller.combine_bgl_and_hba1c_list(userId, _from, _to)  # type: ignore
