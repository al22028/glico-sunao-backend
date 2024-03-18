# Standard Library
from datetime import datetime

# Third Party Library
from pynamodb.attributes import NumberAttribute, UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex
from pynamodb.models import Model
from pynamodb_attributes.unicode_enum import UnicodeEnumAttribute
from schemas.event_timing import EventTiming

DYNAMODB_LOCAL_ENDPOINT = "http://localhost:8000"


class SecondaryIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = "global_secondary_index"
        projection = AllProjection()
        read_capacity_units = 1
        write_capacity_units = 1

    id = UnicodeAttribute(hash_key=True)


class BGLModel(Model):
    class Meta:
        table_name = "bgl"
        region = "ap-northeast-1"
        host = DYNAMODB_LOCAL_ENDPOINT

    id = SecondaryIndex()
    user_id = UnicodeAttribute(hash_key=True)
    value = NumberAttribute(default=0.0)
    event_timing = UnicodeEnumAttribute(enum_type=EventTiming)
    record_time = UTCDateTimeAttribute(default=datetime.now, range_key=True)
    created_at = UTCDateTimeAttribute(default=datetime.now)
    updated_at = UTCDateTimeAttribute(default=datetime.now)


class Hba1cModel(Model):
    class Meta:
        table_name = "hba1c"
        region = "ap-northeast-1"
        host = DYNAMODB_LOCAL_ENDPOINT

    id = SecondaryIndex()
    user_id = UnicodeAttribute(hash_key=True)
    value = NumberAttribute(default=0.0)
    event_timing = UnicodeEnumAttribute(enum_type=EventTiming)
    record_time = UTCDateTimeAttribute(default=datetime.now, range_key=True)
    created_at = UTCDateTimeAttribute(default=datetime.now)
    updated_at = UTCDateTimeAttribute(default=datetime.now)


if __name__ == "__main__":
    if not BGLModel.exists():
        BGLModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)

    if not Hba1cModel.exists():
        Hba1cModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
