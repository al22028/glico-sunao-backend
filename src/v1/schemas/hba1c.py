# Standard Library
from datetime import datetime

# Third Party Library
from pydantic import Field
from schemas.base import BaseSchema
from schemas.event_timing import EventTiming


class Hba1cSchema(BaseSchema):
    id: str = Field(
        ..., title="ID", description="Hba1cデータのID", example="e7b45a9810317095d7ee6748af941d2"  # type: ignore
    )
    user_id: str = Field(
        ..., title="User ID", description="ユーザーのID", example="asds45a98103195d7ee6748af941d2"  # type: ignore
    )
    value: float = Field(
        ..., title="Hba1cの値(%)", description="実際に計測したユーザーのHba1cの値(%)", ge=0.0, example=5.5  # type: ignore
    )
    event_timing: EventTiming = Field(
        ..., title="時間帯", description="ユーザーが計測した時間帯", example=EventTiming.BEFORE_EXERCISE  # type: ignore
    )
    record_time: datetime = Field(
        ...,
        title="記録時間",
        description="ユーザーが計測した時間",
        example="2021-08-21T08:00:00+09:00",  # type: ignore
    )
    is_deleted: bool = Field(
        ...,
        title="削除フラグ",
        description="削除されたかどうかのフラグ",
        example=False,  # type: ignore
    )
    created_at: datetime = Field(
        ..., title="作成日時", description="データが作成された日時", example="2021-08-21T08:00:00+09:00"  # type: ignore
    )
    updated_at: datetime = Field(
        ..., title="更新日時", description="データが最後に更新された日時", example="2021-08-21T08:00:00+09:00"  # type: ignore
    )


class Hba1cCreateRequestSchema(BaseSchema):
    user_id: str = Field(
        ..., title="User ID", description="ユーザーのID", example="asds45a98103195d7ee6748af941d2"  # type: ignore
    )
    value: float = Field(
        ..., title="Hba1cの値(%)", description="実際に計測したユーザーのHba1cの値(%)", ge=0.0, example=5.5  # type: ignore
    )
    event_timing: EventTiming = Field(
        ..., title="時間帯", description="ユーザーが計測した時間帯", example=EventTiming.BEFORE_EXERCISE  # type: ignore
    )
    record_time: datetime = Field(
        ...,
        title="記録時間",
        description="ユーザーが計測した時間",
        example="2021-08-21T08:00:00+09:00",  # type: ignore
    )
