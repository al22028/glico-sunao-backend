# First Party Library
from tests.test_e2e.tag.BGL import BGL
from tests.test_e2e.tag.Hba1c import Hba1c
from tests.test_e2e.tag.User import User

BASE_URL = "https://api.d02.teba-saki.net/v1"

EXAMPLE_DATA_BGL = {
    "value": 89,
    "eventTiming": "食後",
    "recordTime": "2024-06-18T17:46:10.020916",
    "sunaoFood": "パスタ",
    "userId": "6d4c5a63b4b64b1283a4bc4b8f97939d",
}

EXAMPLE_DATA_Hba1c = {
    "value": 5.5,
    "eventTiming": "食後",
    "recordTime": "2024-06-25T00:46:40.748686",
    "sunaoFood": "パスタ",
    "userId": "f4483bf32d89496993bfe28c91941b25",
}

EXAMPLE_DATA_User = {"id": "000001", "termAgreed": False}


def main() -> None:
    bgl = BGL(BASE_URL, EXAMPLE_DATA_BGL)
    bgl.test()

    hba1c = Hba1c(BASE_URL, EXAMPLE_DATA_Hba1c)
    hba1c.test()

    user = User(BASE_URL, EXAMPLE_DATA_User)
    user.test()


if __name__ == "__main__":
    main()
