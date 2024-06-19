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
        return UserModel.scan(UserModel.id == user_id, limit=1).next()

    def is_exist(self, user_id: str) -> bool:
        item = UserModel.scan(UserModel.id == user_id, limit=1)
        try:
            item.next()
            return True
        except StopIteration:
            return False

    def create_one(self, data: UserCreateRequestSchema) -> UserModel:
        term_agreed_at = datetime.now() if data.term_agreed else None
        item = UserModel(id=data.id, term_agreed_at=term_agreed_at, is_deleted=False)
        item.save()
        return item

    def update_term_agreed_at(self, user_id: str) -> UserModel:
        item = self.find_one(user_id)
        item.term_agreed_at = datetime.now()
        item.updated_at = datetime.now()
        item.save()
        return item

    def delete_one(self, user_id: str) -> UserModel:
        item = self.find_one(user_id)
        item.is_deleted = True
        item.updated_at = datetime.now()
        item.save()
        return item
