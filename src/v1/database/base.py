# Standard Library
from datetime import datetime
from uuid import uuid4

# Third Party Library
from pynamodb.attributes import (
    BooleanAttribute,
    NumberAttribute,
    UnicodeAttribute,
    UTCDateTimeAttribute,
)
from pynamodb.models import Model
from pynamodb_attributes.unicode_enum import UnicodeEnumAttribute
from schemas.bgl import BGLSchema
from schemas.hba1c import Hba1cSchema
from schemas.event_timing import EventTiming

# FIXME: This is a temporary solution to use DynamoDB Local
DYNAMODB_LOCAL_ENDPOINT = "http://localhost:8000"


def generate_id() -> str:
    """Generate a unique id

    Returns:
        str: generated id without hyphen
    """
    return str(uuid4()).replace("-", "")


class BGLModel(Model):
    class Meta:
        table_name = "bgl"
        region = "ap-northeast-1"
        host = DYNAMODB_LOCAL_ENDPOINT

    id = UnicodeAttribute(null=False, default=generate_id)
    user_id = UnicodeAttribute(hash_key=True)
    value = NumberAttribute(default=0.0)
    event_timing = UnicodeEnumAttribute(enum_type=EventTiming)
    record_time = UTCDateTimeAttribute(default=datetime.now, range_key=True)
    is_deleted = BooleanAttribute(default=False)
    created_at = UTCDateTimeAttribute(default=datetime.now)
    updated_at = UTCDateTimeAttribute(default=datetime.now)

    def serializer(self) -> BGLSchema:
        serialized_data = {
            "id": self.id,
            "user_id": self.user_id,
            "value": self.value,
            "event_timing": self.event_timing.value,
            "is_deleted": self.is_deleted,
            "record_time": self.record_time.isoformat(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
        return BGLSchema(**serialized_data)

class Hba1cModel(Model):
    class Meta:
        table_name = "hba1c"
        region = "ap-northeast-1"
        host = DYNAMODB_LOCAL_ENDPOINT

    id = UnicodeAttribute(null=False, default=generate_id)
    user_id = UnicodeAttribute(hash_key=True)
    value = NumberAttribute(default=0.0)
    event_timing = UnicodeEnumAttribute(enum_type=EventTiming)
    record_time = UTCDateTimeAttribute(default=datetime.now, range_key=True)
    is_deleted = BooleanAttribute(default=False)
    created_at = UTCDateTimeAttribute(default=datetime.now)
    updated_at = UTCDateTimeAttribute(default=datetime.now)

    def serializer(self) -> Hba1cSchema:
        serialized_data = {
            "id": self.id,
            "user_id": self.user_id,
            "value": self.value,
            "event_timing": self.event_timing.value,
            "is_deleted": self.is_deleted,
            "record_time": self.record_time.isoformat(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
        return Hba1cSchema(**serialized_data)
