# Standard Library
from typing import List

# Third Party Library
from helper.generator import generate_id
from routes.bgl import fetch_bgl_items_by_user_id
from routes.hba1c import fetch_Hba1c_items_by_user_id
from schemas.bgl import BGLSchema
from schemas.bgl_and_hba1c import BGLAndHba1cSchema
from schemas.hba1c import Hba1cSchema


# BGLの要素のみを代入する関数
def make_append_bgl_item(bgl_item: BGLSchema) -> BGLAndHba1cSchema:
    return BGLAndHba1cSchema(
        id=generate_id(),
        record_time=bgl_item.record_time,
        event_timing=bgl_item.event_timing,
        sunao_food=bgl_item.sunao_food,
        bgl_id=bgl_item.id,
        bgl_value=bgl_item.value,
    )


# HbA1cの要素のみを代入する関数
def make_append_hba1c_item(hba1c_item: Hba1cSchema) -> BGLAndHba1cSchema:
    return BGLAndHba1cSchema(
        id=generate_id(),
        record_time=hba1c_item.record_time,
        event_timing=hba1c_item.event_timing,
        sunao_food=hba1c_item.sunao_food,
        bgl_id=hba1c_item.id,
        bgl_value=hba1c_item.value,
    )


class BGLAndHba1cService:

    def combine_bgl_and_hba1c_list(
        self, user_id: str, _from: str, _to: str
    ) -> List[BGLAndHba1cSchema]:

        # BGLとHbA1cデータをfetch
        bgl_items = fetch_bgl_items_by_user_id(user_id, _from, _to)
        hba1c_items = fetch_Hba1c_items_by_user_id(user_id, _from, _to)

        # 日付でソート
        bgl_items = sorted(bgl_items, key=lambda x: x.record_time)
        hba1c_items = sorted(hba1c_items, key=lambda x: x.record_time)

        # BGLとHbA1cを結合したデータを入れるリストを定義
        combined_items: List[BGLAndHba1cSchema] = []

        # BGLかHbA1cどちらかに要素が残っている間
        while bgl_items or hba1c_items:

            # BGLリストが空のとき
            if not bgl_items:
                # HbA1cリストの先頭の要素を挿入
                combined_items.append(make_append_hba1c_item(hba1c_items[0]))
                hba1c_items.pop(0)
                continue

            # HbA1cリストが空のとき
            if not hba1c_items:
                # BGLリストの先頭の要素を挿入
                combined_items.append(make_append_bgl_item(bgl_items[0]))
                bgl_items.pop(0)
                continue

            # 先頭要素の記録時間を取り出す
            bgl_record_time = bgl_items[0].record_time
            hba1c_record_time = hba1c_items[0].record_time

            # 先頭要素の記録時間が同じとき
            # （同じ日時に計測されたBGLとHbA1cの記録時間は
            # 同年同月同日同時00分00秒の形でフロントエンドから登録されている）
            if bgl_record_time == hba1c_record_time:
                # BGLとHbA1cの要素を入れる
                append_item = BGLAndHba1cSchema(
                    id=generate_id(),
                    record_time=bgl_items[0].record_time,
                    event_timing=bgl_items[0].event_timing,
                    sunao_food=bgl_items[0].sunao_food,
                    bgl_id=bgl_items[0].id,
                    bgl_value=bgl_items[0].value,
                    hba1c_id=hba1c_items[0].id,
                    hba1c_value=hba1c_items[0].value,
                )
                combined_items.append(append_item)
                bgl_items.pop(0)
                hba1c_items.pop(0)
                continue

            # BGLデータの記録時間のほうが早いとき
            if bgl_record_time < hba1c_record_time:
                # BGLリストの先頭の要素を挿入
                combined_items.append(make_append_bgl_item(bgl_items[0]))
                bgl_items.pop(0)
                continue
            else:
                # HbA1cリストの先頭の要素を挿入
                combined_items.append(make_append_hba1c_item(hba1c_items[0]))
                hba1c_items.pop(0)
                continue

        return combined_items
