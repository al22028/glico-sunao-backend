from pynamodb.models import Model
from pynamodb.attributes import (UnicodeAttribute, UTCDateTimeAttribute, NumberAttribute)
from datetime import datetime, timedelta, timezone, date

DYNAMODB_LOCAL_ENDPOINT = "http://localhost:8000"


class Hba1cDataModel(Model):
    class Meta:
        table_name = "test-Hba1cdata"
        region = "ap-northeast-1"
        host = DYNAMODB_LOCAL_ENDPOINT

    id = UnicodeAttribute(hash_key=True)
    user_id = UnicodeAttribute(null=False)
    created_at = UTCDateTimeAttribute(null=False)
    updated_at = UTCDateTimeAttribute(null=False)
    record_time = UTCDateTimeAttribute(null=False)
    event_timing = UnicodeAttribute(null=False)
    Hba1c = NumberAttribute(null=False)

if __name__ == "__main__":
    try:
        data = Hba1cDataModel.get("0002")
        print(data.Hba1c)
    except Hba1cDataModel.DoesNotExist:
        print("指定されたキーに対応するアイテムが見つかりませんでした。")
