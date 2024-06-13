# Standard Library
from typing import List
from datetime import datetime

# Third Party Library
from schemas.bgl import BGLSchema
from services.bgl_and_hba1c_service import BGLAndHba1cService


class BGLAndHba1cController:

    def combine_bgl_and_hba1c_list(self, user_id: str, _from: str, _to: str) -> List[BGLSchema]:
        return BGLAndHba1cService().combine_bgl_and_hba1c_list(user_id, _from, _to) # type: ignore
