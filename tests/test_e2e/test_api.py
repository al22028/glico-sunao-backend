# Standard Library
import json

# Third Party Library
import requests  # type: ignore

BASE_URL = "https://api.d02.teba-saki.net/v1"
EXAMPLE_DATA = {
    "value": 89,
    "eventTiming": "食後",
    "recordTime": "2024-06-18T17:46:10.020916",
    "sunaoFood": "パスタ",
    "userId": "6d4c5a63b4b64b1283a4bc4b8f97939d",
}


class BGL:
    def __init__(self) -> None:
        self.endpoint = f"{BASE_URL}/bgl"
        self.example_value = EXAMPLE_DATA
        self.headers = {"Content-Type": "application/json"}
        self.id: str | None = None

    def test_post(self) -> None:
        json_data = json.dumps(self.example_value)
        res = requests.post(self.endpoint, data=json_data, headers=self.headers)
        assert res.status_code == 200, print(res.status_code)
        print("post test passed!")
        self.id = res.json()["id"]

    def test_get_all(self) -> None:
        res = requests.get(self.endpoint)
        assert res.status_code == 200, print(res.status_code)
        print("get all test passed!")

    def test_get(self) -> None:
        if self.id is not None:
            _url = f"{self.endpoint}/{self.id}"
            res = requests.get(_url)
            assert res.status_code == 200, print(res.status_code)
            print("get test passed!")
        else:
            print("ID is not found.")

    def test_get_by_query(self) -> None:
        if self.id is not None:
            _url = f"{self.endpoint}/{self.id}"
            _params = {"userID": self.id, "from": "20240618", "to": "20240718"}
            res = requests.get(_url, params=_params)
            assert res.status_code == 200, print(res.status_code)
            print("get by query test passed!")
        else:
            print("ID is not found.")

    def test_put(self) -> None:
        if self.id is not None:
            _url = f"{self.endpoint}/{self.id}"
            _updated_data = self.example_value.copy()
            _updated_data["sunaoFood"] = "うどん"
            json_data = json.dumps(_updated_data)
            res = requests.put(_url, data=json_data, headers=self.headers)
            assert res.status_code == 200, print(res.status_code)
            print("put test passed!")
        else:
            print("ID is not found.")

    def test_delete(self) -> None:
        if self.id is not None:
            _url = f"{self.endpoint}/{self.id}"
            res = requests.delete(_url)
            assert res.status_code == 200, print(res.status_code)
            print("delete test passed!")
        else:
            print("ID is not found.")

    def test(self) -> None:
        print("[bgl test]")
        try:
            self.test_post()
            self.test_get_all()
            self.test_get()
            self.test_get_by_query()
            self.test_put()
            self.test_delete()
        except AssertionError as a:
            raise (a)


def main() -> None:
    bgl = BGL()
    bgl.test()


if __name__ == "__main__":
    main()
