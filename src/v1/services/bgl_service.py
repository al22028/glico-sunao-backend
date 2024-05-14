# Standard Library
from datetime import datetime
from typing import List

# Third Party Library
from repositories.bgl_repository import BGLRepository
from schemas.bgl import BGLCreateRequestSchema, BGLSchema, BGLUpdateRequestSchema


class BGLService:

    def __init__(self) -> None:
        self.repository = BGLRepository()

    def find_all(self) -> List[BGLSchema]:
        items = self.repository.find_all()
        return [item.serializer() for item in items]

    def find_one(self, id: str) -> BGLSchema:
        data = self.repository.find_one(id)
        return data.serializer()

    def is_exist(self, id: str) -> bool:
        return self.repository.is_exist(id)  # type: ignore

    def create_one(self, data: BGLCreateRequestSchema) -> BGLSchema:
        item = self.repository.create_one(data)
        return item.serializer()

    def delete_one(self, id: str) -> BGLSchema:
        item = self.repository.delete_one(id)
        return item.serializer()

    def update_one(self, id: str, data: BGLUpdateRequestSchema) -> BGLSchema:
        item = self.repository.update_one(id, data)
        return item.serializer()

    def find_many_by_user_id(self, user_id: str, _from: datetime, _to: datetime) -> List[BGLSchema]:
        items = self.repository.find_many_by_user_id(user_id, _from, _to)
        serialized_items: List[BGLSchema] = [item.serializer() for item in items]
        return serialized_items
