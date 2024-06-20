# Standard Library
from datetime import datetime

# Third Party Library
from config.api import STAGE
from helper.generator import generate_id
from pynamodb.attributes import (
    BooleanAttribute,
    NumberAttribute,
    UnicodeAttribute,
    UTCDateTimeAttribute,
)
from pynamodb.models import Model
from pynamodb_attributes.unicode_enum import UnicodeEnumAttribute
from schemas.bgl import BGLSchema
from schemas.event_timing import EventTiming
from schemas.hba1c import Hba1cSchema
from schemas.sunao_foods import SunaoFoods
from schemas.user import UserSchema

# NOTE: This is local endpoint for DynamoDB
DYNAMODB_LOCAL_ENDPOINT = "http://localhost:8000"


class BGLModel(Model):
    class Meta:
        table_name = f"gsp_{STAGE}_sbr_bgl_table"
        region = "ap-northeast-1"
        if STAGE == "local":
            host = DYNAMODB_LOCAL_ENDPOINT

    id = UnicodeAttribute(null=False, default=generate_id)
    user_id = UnicodeAttribute(hash_key=True)
    value = NumberAttribute(default=0.0)
    event_timing = UnicodeEnumAttribute(enum_type=EventTiming)
    record_time = UTCDateTimeAttribute(default=datetime.now, range_key=True)
    sunao_food = UnicodeEnumAttribute(enum_type=SunaoFoods, null=True, default=None)
    is_deleted = BooleanAttribute(default=False)
    created_at = UTCDateTimeAttribute(default=datetime.now)
    updated_at = UTCDateTimeAttribute(default=datetime.now)

    def serializer(self) -> BGLSchema:
        serialized_data = {
            "id": self.id,
            "user_id": self.user_id,
            "value": self.value,
            "event_timing": self.event_timing.value,
            "sunao_food": self.sunao_food,
            "is_deleted": self.is_deleted,
            "record_time": self.record_time.isoformat(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
        return BGLSchema(**serialized_data)


class Hba1cModel(Model):
    class Meta:
        table_name = f"gsp_{STAGE}_sbr_hba1c_table"
        region = "ap-northeast-1"
        if STAGE == "local":
            host = DYNAMODB_LOCAL_ENDPOINT

    id = UnicodeAttribute(null=False, default=generate_id)
    user_id = UnicodeAttribute(hash_key=True)
    value = NumberAttribute(default=0.0)
    event_timing = UnicodeEnumAttribute(enum_type=EventTiming)
    record_time = UTCDateTimeAttribute(default=datetime.now, range_key=True)
    sunao_food = UnicodeEnumAttribute(enum_type=SunaoFoods, null=True, default=None)
    is_deleted = BooleanAttribute(default=False)
    created_at = UTCDateTimeAttribute(default=datetime.now)
    updated_at = UTCDateTimeAttribute(default=datetime.now)

    def serializer(self) -> Hba1cSchema:
        serialized_data = {
            "id": self.id,
            "user_id": self.user_id,
            "value": self.value,
            "event_timing": self.event_timing.value,
            "sunao_food": self.sunao_food,
            "is_deleted": self.is_deleted,
            "record_time": self.record_time.isoformat(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
        return Hba1cSchema(**serialized_data)


class UserModel(Model):
    class Meta:
        table_name = f"gsp_{STAGE}_sbr_user_table"
        region = "ap-northeast-1"
        if STAGE == "local":
            host = DYNAMODB_LOCAL_ENDPOINT

    id = UnicodeAttribute(null=False, hash_key=True)
    term_agreed_at = UTCDateTimeAttribute(null=True, default=None)
    is_deleted = BooleanAttribute(default=False)
    created_at = UTCDateTimeAttribute(default=datetime.now)
    updated_at = UTCDateTimeAttribute(default=datetime.now)

    def serializer(self) -> UserSchema:
        serialized_data = {
            "id": self.id,
            "term_agreed": True if self.term_agreed_at else False,
            "term_agreed_at": self.term_agreed_at.isoformat() if self.term_agreed_at else None,
            "is_deleted": self.is_deleted,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
        return UserSchema(**serialized_data)
