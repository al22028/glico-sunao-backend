# Standard Library
from datetime import datetime
from typing import List

# Third Party Library
from aws_lambda_powertools.event_handler.exceptions import NotFoundError
from database.base import Hba1cModel
from schemas.hba1c import Hba1cCreateRequestSchema, Hba1cUpdateRequestSchema


def is_not_deleted(item: Hba1cModel) -> bool:
    return not item.is_deleted


class Hba1cModelORM:
    #
    def find_all(self) -> List[Hba1cModel]:
        items = Hba1cModel.scan()
        return [item for item in items if not item.is_deleted]

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

    # NOTE: record time is sortkey, so we can't update it
    def update_one(self, id: str, data: Hba1cUpdateRequestSchema) -> Hba1cModel:
        item = self.find_one(id)
        item.update(
            actions=[
                Hba1cModel.value.set(data.value),
                Hba1cModel.event_timing.set(data.event_timing),
                # Hba1cModel.record_time.set(datetime.now()),
                Hba1cModel.updated_at.set(datetime.now()),
            ]
        )
        return item

    def delete_one(self, id: str) -> Hba1cModel:
        item = self.find_one(id)
        item.is_deleted = True
        item.save()
        return item

    def find_many_by_user_id(
        self, user_id: str, _from: datetime, _to: datetime
    ) -> List[Hba1cModel]:
        items = Hba1cModel.query(
            hash_key=user_id, range_key_condition=Hba1cModel.record_time.between(_from, _to)
        )
        return [item for item in items if not item.is_deleted]
