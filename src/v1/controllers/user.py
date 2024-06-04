# Standard Library
from typing import List

# Third Party Library
from schemas.user import UserSchema
from services.user_service import UserService


class UserController:

    def __init__(self) -> None:
        self.service = UserService()

    def find_all(self) -> List[UserSchema]:
        return self.service.find_all()  # type: ignore
