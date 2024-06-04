# Standard Library
from typing import List

# Third Party Library
from schemas.user import UserCreateRequestSchema, UserSchema
from services.user_service import UserService


class UserController:

    def __init__(self) -> None:
        self.service = UserService()

    def find_all(self) -> List[UserSchema]:
        return self.service.find_all()  # type: ignore

    def find_one(self, id: str) -> UserSchema:
        return self.service.find_one(id)

    def create_one(self, data: UserCreateRequestSchema) -> UserSchema:
        return self.service.create_one(data)
