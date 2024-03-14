from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute

from faker import Faker

DYNAMODB_LOCAL_ENDPOINT = "http://localhost:8000"


class UserModel(Model):
    class Meta:
        table_name = "users"
        region = "ap-northeast-1"
        host = DYNAMODB_LOCAL_ENDPOINT

    id = UnicodeAttribute(hash_key=True)
    email = UnicodeAttribute(null=False)
    username = UnicodeAttribute(null=False)
    first_name = UnicodeAttribute(null=False)
    last_name = UnicodeAttribute(null=False)


if not UserModel.exists():
    UserModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)


faker = Faker(locale="ja_JP")


if __name__ == "__main__":
    for _ in range(10):
        UserModel(
            id=faker.uuid4(),
            email=faker.email(),
            username=faker.user_name(),
            first_name=faker.first_name(),
            last_name=faker.last_name(),
        ).save()
