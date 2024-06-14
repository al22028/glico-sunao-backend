# Standard Library
from datetime import datetime

# Third Party Library
from helper.generator import generate_id
from pydantic import Field
from schemas.base import BaseSchema
from schemas.event_timing import EventTiming
from schemas.sunao_foods import SunaoFoods


class BGLAndHba1cSchema(BaseSchema):
    id: str = Field(
        ...,
        title="血糖値とHbA1cを合わせたデータのID",
        description="血糖値とHbA1cを合わせたデータのID",
        example=generate_id(),  # type: ignore
    )
    record_time: datetime = Field(
        ...,
        title="記録時間",
        description="ユーザーが計測した時間",
        example=datetime.now().isoformat(),  # type: ignore
    )
    event_timing: EventTiming = Field(
        ...,
        title="時間帯",
        description="ユーザーが計測した時間帯",
        example=EventTiming.AFTER_MEAL,  # type: ignore
    )
    sunao_food: SunaoFoods | None = Field(
        default=None,
        title="SUNAO商品の摂取",
        description="SUNAO商品の摂取の有無。血糖値データのsunao_foodを参照する",
        example=SunaoFoods.PASTA,  # type: ignore
    )
    bgl_id: str | None = Field(
        default=None,
        title="血糖値ID",
        description="血糖値データのID",
        example=generate_id(),  # type: ignore
    )
    bgl_value: float | None = Field(
        default=None,
        title="血糖値の値(mg/dl)",
        description="実際に計測したユーザーの血糖値の値",
        ge=0.0,
        example=89.0,  # type: ignore
    )
    hba1c_id: str | None = Field(
        default=None,
        title="HbA1cID",
        description="Hba1cデータのID",
        example=generate_id(),  # type: ignore
    )
    hba1c_value: float | None = Field(
        default=None,
        title="Hba1cの値(%)",
        description="実際に計測したユーザーのHba1cの値(%)",
        ge=0.0,
        example=5.5,  # type: ignore
    )
