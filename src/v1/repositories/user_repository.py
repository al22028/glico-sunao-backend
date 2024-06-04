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

    def find_one(self, user_id: str) -> UserModel:
        return UserModel.scan(UserModel.user_id == user_id, limit=1).next()

    def create_one(self, data: UserCreateRequestSchema) -> UserModel:
        item = UserModel(**data.model_dump())
        item.save()
        return item

    def update_term_agreed_at(self, user_id: str) -> UserModel:
        item = self.find_one(user_id)
        item.term_agreed = True
        item.term_agreed_at = datetime.now()
        item.save()
        return item
