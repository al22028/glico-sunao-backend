# Standard Library
from datetime import datetime, timedelta
from typing import List

# Third Party Library
from database.base import Hba1cModel
from schemas.hba1c import Hba1cCreateRequestSchema, Hba1cUpdateRequestSchema


class Hba1cRepository:

    def find_all(self) -> List[Hba1cModel]:
        items = Hba1cModel.scan()
        return [item for item in items if not item.is_deleted]

    def create_one(self, data: Hba1cCreateRequestSchema) -> Hba1cModel:
        item = Hba1cModel(**data.model_dump())
        item.save()
        return item

    def is_exist(self, id: str) -> bool:
        item = Hba1cModel.scan(Hba1cModel.id == id, limit=1)
        try:
            item.next()
            return True
        except StopIteration:
            return False

    def find_one(self, id: str) -> Hba1cModel:
        return Hba1cModel.scan(Hba1cModel.id == id, limit=1).next()

    def update_one(self, id: str, data: Hba1cUpdateRequestSchema) -> Hba1cModel:
        item = self.find_one(id)
        user_id = item.user_id
        item.delete()
        item = Hba1cModel(**data.model_dump(), user_id=user_id)
        item.save()
        return item

    def delete_one(self, id: str) -> Hba1cModel:
        item = self.find_one(id)
        item.is_deleted = True
        item.save()
        return item

    def find_many_by_user_id(
        self, user_id: str, _from: datetime, _to: datetime
    ) -> List[Hba1cModel]:
        adjusted_to = _to + timedelta(days=1)
        items = Hba1cModel.query(
            hash_key=user_id, range_key_condition=Hba1cModel.record_time.between(_from, adjusted_to)
        )
        return [item for item in items if not item.is_deleted]
