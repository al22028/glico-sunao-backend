# Standard Library
from typing import List

# Third Party Library
from aws_lambda_powertools.event_handler.exceptions import NotFoundError
from schemas.hba1c import Hba1cCreateRequestSchema, Hba1cSchema, Hba1cUpdateRequestSchema
from services.hba1c_service import Hba1cService


class Hba1cController:

    def __init__(self) -> None:
        self.service = Hba1cService()

    def find_all(self) -> List[Hba1cSchema]:
        return self.service.find_all()  # type: ignore

    def find_one(self, id: str) -> Hba1cSchema:
        if not self.service.is_exist(id):
            raise NotFoundError("Hba1c not found.")
        return self.service.find_one(id)

    def create_one(self, data: Hba1cCreateRequestSchema) -> Hba1cSchema:
        return self.service.create_one(data)

    def update_one(self, id: str, data: Hba1cUpdateRequestSchema) -> Hba1cSchema:
        if not self.service.is_exist(id):
            raise NotFoundError("Hba1c not found.")
        return self.service.update_one(id, data)

    def delete_one(self, id: str) -> Hba1cSchema:
        if not self.service.is_exist(id):
            raise NotFoundError("Hba1c not found.")
        return self.service.delete_one(id)

    def find_many_by_user_id(self, user_id: str, _from: str, _to: str) -> List[Hba1cSchema]:
        return self.service.find_many_by_user_id(user_id, _from, _to)  # type: ignore
