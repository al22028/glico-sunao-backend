# Third Party Library
from schemas.base import BaseSchema


class BGLSchema(BaseSchema):
    id: str
    user_id: str
    value: float
    event_timing: str
    record_time: str
    created_at: str
    updated_at: str
