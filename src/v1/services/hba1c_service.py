# Standard Library
from datetime import datetime
from typing import List

# Third Party Library
from repositories.hba1c_repository import Hba1cRepository
from schemas.hba1c import Hba1cCreateRequestSchema, Hba1cSchema, Hba1cUpdateRequestSchema


class Hba1cService:

    def __init__(self) -> None:
        self.repository = Hba1cRepository()

    def find_all(self) -> List[Hba1cSchema]:
        items = self.repository.find_all()
        return [item.serializer() for item in items]

    def find_one(self, id: str) -> Hba1cSchema:
        data = self.repository.find_one(id)
        return data.serializer()

    def is_exist(self, id: str) -> bool:
        return self.repository.is_exist(id)  # type: ignore

    def create_one(self, data: Hba1cCreateRequestSchema) -> Hba1cSchema:
        item = self.repository.create_one(data)
        return item.serializer()

    def delete_one(self, id: str) -> Hba1cSchema:
        item = self.repository.delete_one(id)
        return item.serializer()

    def update_one(self, id: str, data: Hba1cUpdateRequestSchema) -> Hba1cSchema:
        item = self.repository.update_one(id, data)
        return item.serializer()

    def find_many_by_user_id(
        self, user_id: str, _from: datetime, _to: datetime
    ) -> List[Hba1cSchema]:
        items = self.repository.find_many_by_user_id(user_id, _from, _to)
        serialized_items: List[Hba1cSchema] = [item.serializer() for item in items]
        return serialized_items
