# Standard Library
from typing import List

# Third Party Library
from aws_lambda_powertools.event_handler.exceptions import NotFoundError
from schemas.bgl import BGLCreateRequestSchema, BGLSchema, BGLUpdateRequestSchema
from services.bgl_service import BGLService


class BGLController:

    def __init__(self) -> None:
        self.service = BGLService()

    def find_all(self) -> List[BGLSchema]:
        return self.service.find_all()  # type: ignore

    def find_one(self, id: str) -> BGLSchema:
        if not self.service.is_exist(id):
            raise NotFoundError("BGL not found.")
        return self.service.find_one(id)

    def create_one(self, data: BGLCreateRequestSchema) -> BGLSchema:
        return self.service.create_one(data)

    def update_one(self, id: str, data: BGLUpdateRequestSchema) -> BGLSchema:
        if not self.service.is_exist(id):
            raise NotFoundError("BGL not found.")
        return self.service.update_one(id, data)

    def delete_one(self, id: str) -> BGLSchema:
        if not self.service.is_exist(id):
            raise NotFoundError("BGL not found.")
        return self.service.delete_one(id)

    def find_many_by_user_id(self, user_id: str, _from: str, _to: str) -> List[BGLSchema]:
        return self.service.find_many_by_user_id(user_id, _from, _to)  # type: ignore
