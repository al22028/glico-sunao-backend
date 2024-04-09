# Standard Library
from datetime import datetime
from typing import List

# Third Party Library
from aws_lambda_powertools.event_handler.exceptions import NotFoundError
from database.base import BGLModel
from schemas.bgl import BGLCreateRequestSchema, BGLUpdateRequestSchema


class BGLModelORM:

    def find_all(self) -> List[BGLModel]:
        items = BGLModel.scan()
        return [item for item in items if not item.is_deleted]

    def create_one(self, data: BGLCreateRequestSchema) -> BGLModel:
        item = BGLModel(**data.model_dump())
        item.save()
        return item

    def find_one(self, id: str) -> BGLModel:
        item = BGLModel.scan(BGLModel.id == id, limit=1)
        try:
            return item.next()
        except StopIteration:
            raise NotFoundError(f"BGL data not found with id: {id}")

    # NOTE: record time is sortkey, so we can't update it
    def update_one(self, id: str, data: BGLUpdateRequestSchema) -> BGLModel:
        item = self.find_one(id)
        item.update(
            actions=[
                BGLModel.value.set(data.value),
                BGLModel.event_timing.set(data.event_timing),
                # BGLModel.record_time.set(datetime.now()),
                BGLModel.updated_at.set(datetime.now()),
            ]
        )
        return item

    def delete_one(self, id: str) -> BGLModel:
        item = self.find_one(id)
        item.is_deleted = True
        item.save()
        return item

    def find_many_by_user_id(self, user_id: str, _from: datetime, _to: datetime) -> List[BGLModel]:
        items = BGLModel.query(
            hash_key=user_id, range_key_condition=BGLModel.record_time.between(_from, _to)
        )
        return [item for item in items if not item.is_deleted]
