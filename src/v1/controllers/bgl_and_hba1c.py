# Standard Library
from typing import List

# Third Party Library
from schemas.bgl_and_hba1c import BGLAndHba1cSchema
from services.bgl_and_hba1c_service import BGLAndHba1cService


class BGLAndHba1cController:

    def combine_bgl_and_hba1c_list(
        self, user_id: str, _from: str, _to: str
    ) -> List[BGLAndHba1cSchema]:
        return BGLAndHba1cService().combine_bgl_and_hba1c_list(user_id, _from, _to)  # type: ignore
