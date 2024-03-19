from pynamodb.models import Model
from pynamodb.attributes import (UnicodeAttribute, UTCDateTimeAttribute, NumberAttribute)
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
    created_at = UTCDateTimeAttribute(null=False)
    updated_at = UTCDateTimeAttribute(null=False)
    record_time = UTCDateTimeAttribute(null=False)
    event_timing = UnicodeAttribute(null=False)
    blood_glucose_level = NumberAttribute(null=False)

if __name__ == "__main__":
    try:
        data = BGLDataModel.get("0002")
        print(data.blood_glucose_level)
    except BGLDataModel.DoesNotExist:
        print("指定されたキーに対応するアイテムが見つかりませんでした。")
