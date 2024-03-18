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
    data = BGLDataModel.get("0001")
    print(data.blood_glucose_level)
