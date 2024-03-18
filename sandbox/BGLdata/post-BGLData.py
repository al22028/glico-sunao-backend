from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from faker import Faker
from datetime import datetime, timedelta, timezone
from datetime import date

DYNAMODB_LOCAL_ENDPOINT = "http://localhost:8000"


class BGLDataModel(Model):
    class Meta:
        table_name = "test-BGLdata"
        region = "ap-northeast-1"
        host = DYNAMODB_LOCAL_ENDPOINT

    id = UnicodeAttribute(hash_key=True)
    user_id = UnicodeAttribute(null=False)
    created_at = UnicodeAttribute(null=False)
    updated_at = UnicodeAttribute(null=False)
    record_time = UnicodeAttribute(null=False)
    event_timing = UnicodeAttribute(null=False)
    blood_glucose_level = UnicodeAttribute(null=False)


if not BGLDataModel.exists():
    BGLDataModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)


faker = Faker(locale="ja_JP")


if __name__ == "__main__":
    BGLDataModel(
        id = "0001",
        user_id = "35c9fa54-6617-431d-abdf-b376c642cda5",
        created_at = round(datetime.now().timestamp()),
        updated_at = round(datetime.now().timestamp()),
        record_time = round(datetime.now().timestamp()),
        event_timing = "起床",
        blood_glucose_level = 100
    ).save()
