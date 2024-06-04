# Standard Library
from typing import List

# Third Party Library
from database.base import UserModel
from schemas.user import UserCreateRequestSchema


class UserRepository:

    def find_all(self) -> List[UserModel]:
        items = UserModel.scan()
        return list(items)

    def create_one(self, data: UserCreateRequestSchema) -> UserModel:
        item = UserModel(**data.model_dump())
        item.save()
        return item
