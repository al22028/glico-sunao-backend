# Standard Library
from typing import List

# Third Party Library
from database.base import UserModel

class UserRepository:

    def find_all(self) -> List[UserModel]:
        items = UserModel.scan()
        return list(items)
