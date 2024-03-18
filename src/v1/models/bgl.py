# Standard Library
from typing import List

# Third Party Library
from database.base import BGLModel


class BGLModelORM:

    def find_all(self) -> List[BGLModel]:
        items = BGLModel.scan()
        return [item for item in items]
