import json


import requests


def get_price(service_url: str, item: str):
    payload = {"code":item}
    response = requests.post(service_url, data=json.dumps(payload))
    return json.loads(response.text)


if __name__ == '__main__':
    print(
        get_price("http://localhost:8000/price", "paper")
    )
