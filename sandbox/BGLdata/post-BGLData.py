from pynamodb.models import Model
from pynamodb.attributes import (UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute)
from datetime import datetime, timedelta, timezone, date

DYNAMODB_LOCAL_ENDPOINT = "http://localhost:8000"

class BGLDataModel(Model):
    class Meta:
        table_name = "test-BGLdata"
        region = "ap-northeast-1"
        host = DYNAMODB_LOCAL_ENDPOINT

    id = UnicodeAttribute(hash_key=True)
    user_id = UnicodeAttribute(null=False)
    created_at = UnicodeAttribute(null=False)
    updated_at = UTCDateTimeAttribute(null=False)
    record_time = UTCDateTimeAttribute(null=False)
    event_timing = UnicodeAttribute(null=False)
    blood_glucose_level = NumberAttribute(null=False)


if not BGLDataModel.exists():
    BGLDataModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)

if __name__ == "__main__":
    current_time_utc = datetime.now(timezone.utc)
    jst = timezone(timedelta(hours=-9))
    current_time_jst = current_time_utc.astimezone(jst)

    BGLDataModel(
        id = "0010",
        user_id = "35c9fa54-6617-431d-abdf-b376c642cda5",
        created_at = datetime.now().isoformat(),
        updated_at = current_time_jst,
        record_time = current_time_jst,
        event_timing = "起床",
        blood_glucose_level = 100.5
    ).save()
