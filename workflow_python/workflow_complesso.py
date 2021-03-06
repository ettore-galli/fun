from __future__ import annotations
from dataclasses import dataclass

import os
from typing import List, Optional, Any, Callable, Dict

from services.config import read_config
from services.order import get_order
from services.exchange import get_exchange
from services.price import get_price
from services.writer import write_output

'''
IO Come valore
Composizione / Concatenamento
Lazy -> un effetto non è tale finchè non avviene
-> barare + procrastinare
'''
class WorkflowPayload:

    def __init__(self, config: Optional[Any] = None, data: Optional[Any] = None):
        self.data: Optional[Any] = data
        self.config: Optional[Any] = config

    def __repr__(self):
        return str(self.config) + str(self.data)

    def clone(self, config: Optional[Any] = None, data: Optional[Any] = None):
        return WorkflowPayload(config=config if config is not None else self.config, data=data if data is not None else self.data)

    @classmethod
    def unit(cls, config: Optional[Any] = None, data: Optional[Any] = None):
        return WorkflowPayload(config, data)

    def bind(self, f: Callable[[WorkflowPayload], WorkflowPayload]):
        return f(self.clone())

    def __rshift__(self, other):
        return self.bind(other)


def read_config_action(payload: WorkflowPayload) -> WorkflowPayload:
    return payload.clone(config=read_config("./cfg/config.ini"))


def read_order_action(payload: WorkflowPayload) -> WorkflowPayload:
    return payload.clone(data=get_order(service_url=payload.config["orders_url"], order_number=1))


def retrieve_prices_action(payload: WorkflowPayload) -> WorkflowPayload:
    priced_order = [
        {
            **line,
            **get_price(service_url=payload.config["price_url"], item=line["item"])
        }
        for line in payload.data
    ]
    return payload.clone(data=priced_order)


def retrieve_exchange_action(payload: WorkflowPayload) -> WorkflowPayload:
    target_currency = "EUR"
    normalized_order = [
        {
            **line,
            "price": line["price"] * get_exchange(service_url=payload.config["exchange_url"], from_currency=line["currency"], to_currency=target_currency),
            "currency": target_currency
        }
        for line in payload.data
    ]
    return payload.clone(data=normalized_order)


if __name__ == "__main__":
    print(os.path.abspath("."))
    print(
        WorkflowPayload.unit()
        .bind(read_config_action)
        .bind(read_order_action)
        .bind(retrieve_prices_action)
        .bind(retrieve_exchange_action)
    )

    mocked_config = {
        'input_file': 'input/list.txt',
        'output_directory': 'output',
        'output_file_prefix': 'OUT',
        'orders_url': 'http://localhost:8000/orders/order_number',
        'price_url': 'http://localhost:8000/price',
        'exchange_url': 'http://localhost:8000/exchange'
    }
    
    print(
        WorkflowPayload.unit(config=mocked_config)
        .bind(read_order_action)
        .bind(retrieve_prices_action)
        .bind(retrieve_exchange_action)
    )
