# Standard Library
from datetime import datetime
from typing import List

# Third Party Library
from database.base import UserModel
from schemas.user import UserCreateRequestSchema


class UserRepository:

    def find_all(self) -> List[UserModel]:
        items = UserModel.scan()
        return list(items)

    def find_one(self, id: str) -> UserModel:
        return UserModel.scan(UserModel.id == id, limit=1).next()

    def create_one(self, data: UserCreateRequestSchema) -> UserModel:
        item = UserModel(**data.model_dump())
        item.save()
        return item

    def update_agreed_at(self, id: str) -> UserModel:
        item = self.find_one(id)
        item.agreed_at = datetime.now()
        item.save()
        return item
