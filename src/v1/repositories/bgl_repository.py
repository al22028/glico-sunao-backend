# Standard Library
from datetime import datetime, timedelta
from typing import List

# Third Party Library
from database.base import BGLModel
from schemas.bgl import BGLCreateRequestSchema, BGLUpdateRequestSchema


class BGLRepository:

    def find_all(self) -> List[BGLModel]:
        items = BGLModel.scan()
        return list(items)

    def create_one(self, data: BGLCreateRequestSchema) -> BGLModel:
        item = BGLModel(**data.model_dump())
        item.save()
        return item

    def is_exist(self, id: str) -> bool:
        item = BGLModel.scan(BGLModel.id == id, limit=1)
        try:
            item.next()
            return True
        except StopIteration:
            return False

    def find_one(self, id: str) -> BGLModel:
        return BGLModel.scan(BGLModel.id == id, limit=1).next()

    def update_one(self, id: str, data: BGLUpdateRequestSchema) -> BGLModel:
        item = self.find_one(id)
        user_id = item.user_id
        id = item.id
        created_at = item.created_at
        item.delete()
        item = BGLModel(**data.model_dump(), user_id=user_id, id=id, created_at=created_at)
        item.save()
        return item

    def delete_one(self, id: str) -> BGLModel:
        item = self.find_one(id)
        item.is_deleted = True
        item.save()
        return item

    def find_many_by_user_id(self, user_id: str, _from: datetime, _to: datetime) -> List[BGLModel]:
        adjusted_to = _to + timedelta(days=1)
        items = BGLModel.query(
            hash_key=user_id, range_key_condition=BGLModel.record_time.between(_from, adjusted_to)
        )
        return [item for item in items if not item.is_deleted]
