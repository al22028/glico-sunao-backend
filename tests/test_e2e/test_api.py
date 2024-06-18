# Standard Library
import json

# Third Party Library
import requests

BASE_URL = "https://api.d02.teba-saki.net"
EXAMPLE_DATA = {
  "value": 89,
  "eventTiming": "食後",
  "recordTime": "2024-06-18T17:46:10.020916",
  "sunaoFood": "パスタ",
  "userId": "6d4c5a63b4b64b1283a4bc4b8f97939d"
}


class BGL:
    def __init__(self) -> None:
        self.endpoint = f"{BASE_URL}/bgl"
        self.example_value = EXAMPLE_DATA
        self.id = None

    def get_all_test(self) -> None:
        res = requests.get(self.endpoint)
        print(res)

    def get_test(self) -> None:
        if self.id != None:
            _url = f"{self.endpoint}/{self.id}"
            res = requests.get(_url)
            if res.status_code == 200:
                print(f"get request: {res}")
            else:
                print(res.json())
        else:
            print("ID is not found.")

    def post_test(self) -> None:
        headers = {"Content-Type": "application/json"}
        json_data = json.dumps(self.example_value)
        res = requests.post(self.endpoint, data=json_data, headers=headers)
        if res.status_code == 201:
            self.id = res.json()["id"]
            print(self.id)

    def delete_test(self) -> None:
        if self.id != None:
            _url = f"{self.endpoint}/{self.id}"
            res = requests.delete(_url)
            if res.status_code == 200:
                print(f"delete request: {res}")
            else:
                print(res.json())
        else:
            print("ID is not found.")

    def test(self) -> None:
        try:
            self.post_test()
            self.get_test()
            self.delete_test()
        except RuntimeError as e:
            raise(e)

def main() -> None:
    bgl = BGL()
    bgl.test()



if __name__ == "__main__":
    main()
