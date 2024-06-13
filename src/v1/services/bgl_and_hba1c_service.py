# Standard Library
from typing import List
from datetime import datetime

# Third Party Library
from schemas.bgl_and_hba1c import BGLAndHba1cSchema
from schemas.bgl import BGLSchema
from routes.bgl import fetch_bgl_items_by_user_id
from routes.hba1c import fetch_Hba1c_items_by_user_id

class BGLAndHba1cService:

    def combine_bgl_and_hba1c_list(self, user_id: str, _from: str, _to: str) -> List[BGLSchema]:
        bgl_items = fetch_bgl_items_by_user_id(user_id, _from, _to)
        hba1c_items = fetch_Hba1c_items_by_user_id(user_id, _from, _to)

        bgl_items = sorted(bgl_items, key=lambda x:x.record_time)
        hba1c_items = sorted(hba1c_items, key=lambda x:x.record_time)

        return bgl_items # type: ignore
