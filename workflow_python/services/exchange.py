import json


import requests


def get_exchange(service_url: str, from_currency: str, to_currency: str):
    payload = {
        "from_currency": {
            "code": from_currency
        },
        "to_currency": {
            "code": to_currency
        }
    }
    response = requests.post(service_url, data=json.dumps(payload))
    return json.loads(response.text)["exchange_ratio"]


if __name__ == '__main__':
    print(
        get_exchange("http://localhost:8000/exchange", "USD", "JPY")
    )
