# Standard Library
from typing import List

# Third Party Library
from repositories.user_repository import UserRepository
from schemas.user import UserSchema

class UserService:

    def __init__(self) -> None:
        self.repository = UserRepository()

    def find_all(self) -> List[UserSchema]:
        items = self.repository.find_all()
        return [item.serializer() for item in items]
