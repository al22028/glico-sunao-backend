# Standard Library
from typing import List

# Third Party Library
from repositories.user_repository import UserRepository
from schemas.user import UserCreateRequestSchema, UserSchema


class UserService:

    def __init__(self) -> None:
        self.repository = UserRepository()

    def find_all(self) -> List[UserSchema]:
        items = self.repository.find_all()
        return [item.serializer() for item in items]

    def find_one(self, id: str) -> UserSchema:
        data = self.repository.find_one(id)
        return data.serializer()

    def create_one(self, data: UserCreateRequestSchema) -> UserSchema:
        item = self.repository.create_one(data)
        return item.serializer()
