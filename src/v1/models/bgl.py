# Standard Library
from typing import List

# Third Party Library
from aws_lambda_powertools.event_handler.exceptions import NotFoundError
from database.base import BGLModel
from schemas.bgl import BGLCreateRequestSchema


class BGLModelORM:

    def find_all(self) -> List[BGLModel]:
        items = BGLModel.scan()
        return [item for item in items]

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
