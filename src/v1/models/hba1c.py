# Standard Library
from datetime import datetime
from typing import List

# Third Party Library
from aws_lambda_powertools.event_handler.exceptions import NotFoundError
from database.base import Hba1cModel
from schemas.hba1c import Hba1cCreateRequestSchema


class Hba1cModelORM:

    def find_all(self) -> List[Hba1cModel]:
        items = Hba1cModel.scan()
        return [item for item in items]

    def create_one(self, data: Hba1cCreateRequestSchema) -> Hba1cModel:
        item = Hba1cModel(**data.model_dump())
        item.save()
        return item

    def find_one(self, id: str) -> Hba1cModel:
        item = Hba1cModel.scan(Hba1cModel.id == id, limit=1)
        try:
            return item.next()
        except StopIteration:
            raise NotFoundError(f"Hba1c data not found with id: {id}")

    def update_one(self, id: str, data: Hba1cCreateRequestSchema) -> Hba1cModel:
        item = self.find_one(id)
        item.value = data.value
        item.event_timing = data.event_timing.value
        item.record_time = data.record_time
        item.save()
        return item

    def delete_one(self, id: str) -> Hba1cModel:
        item = self.find_one(id)
        item.is_deleted = True
        item.save()
        return item

    def find_many_by_user_id(self, user_id: str, _from: datetime, _to: datetime) -> List[Hba1cModel]:
        items = Hba1cModel.query(
            hash_key=user_id, range_key_condition=Hba1cModel.record_time.between(_from, _to)
        )
        return [item for item in items]
