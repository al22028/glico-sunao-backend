# Standard Library
import json

# Third Party Library
import requests  # type: ignore

# First Party Library
from tests.test_e2e.cprint import cprint


class Hba1c:
    def __init__(self, base_url: str, example_data: dict) -> None:
        self.endpoint = f"{base_url}/hba1c"
        self.example_value = example_data
        self.headers = {"Content-Type": "application/json"}
        self.id: str | None = None

    def test_post(self) -> None:
        json_data = json.dumps(self.example_value)
        res = requests.post(self.endpoint, data=json_data, headers=self.headers)
        assert res.status_code == 200, print(res.status_code)
        cprint("green", "post test passed!")
        self.id = res.json()["id"]

    def test_get_all(self) -> None:
        res = requests.get(self.endpoint)
        assert res.status_code == 200, print(res.status_code)
        cprint("green", "get all test passed!")

    def test_get(self) -> None:
        if self.id is not None:
            _url = f"{self.endpoint}/{self.id}"
            res = requests.get(_url)
            assert res.status_code == 200, print(res.status_code)
            cprint("green", "get test passed!")
        else:
            print("ID is not found.")

    def test_get_by_query(self) -> None:
        if self.id is not None:
            _url = f"{self.endpoint}/{self.id}"
            _params = {"userID": self.id, "from": "20240618", "to": "20240718"}
            res = requests.get(_url, params=_params)
            assert res.status_code == 200, print(res.status_code)
            cprint("green", "get by query test passed!")
        else:
            print("ID is not found.")

    def test_put(self) -> None:
        if self.id is not None:
            _url = f"{self.endpoint}/{self.id}"
            _updated_data = self.example_value.copy()
            json_data = json.dumps(_updated_data)
            res = requests.put(_url, data=json_data, headers=self.headers)
            assert res.status_code == 200, print(res.status_code)
            cprint("green", "put test passed!")
        else:
            print("ID is not found.")

    def test_delete(self) -> None:
        if self.id is not None:
            _url = f"{self.endpoint}/{self.id}"
            res = requests.delete(_url)
            assert res.status_code == 200, print(res.status_code)
            cprint("green", "delete test passed!")
        else:
            print("ID is not found.")

    def test(self) -> None:
        cprint("blue", "[Hba1c]")
        try:
            self.test_post()
            self.test_get_all()
            self.test_get()
            self.test_get_by_query()
            self.test_put()
            self.test_delete()
        except AssertionError as a:
            raise (a)
