# Standard Library
from datetime import datetime

# Third Party Library
from schemas.base import BaseSchema
from schemas.event_timing import EventTiming


class BGLSchema(BaseSchema):
    id: str
    user_id: str
    value: float
    event_timing: str
    record_time: str
    is_deleted: bool
    created_at: str
    updated_at: str


class BGLCreateRequestSchema(BaseSchema):
    user_id: str
    value: float
    event_timing: EventTiming
    record_time: datetime
