import json


import requests


def get_order(service_url: str, order_number: int):
    query_url = service_url.replace("#order_number", str(order_number))
    print(query_url)
    response = requests.get(query_url)
    return json.dumps(json.loads(response.text))


if __name__ == '__main__':
    print(
        get_order("http://localhost:8000/orders/#order_number", 2)
    )
