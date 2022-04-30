from typing import List
from pydantic import BaseModel


class Currency(BaseModel):
    code: str


class Exchange(BaseModel):
    exchange_ratio: float


EXCHANGE_VS_EUR = {
    "EUR": 1.0,
    "USD": 1.05,
    "JPY": 136.93,
    "CHF": 1.02
}


def calculate_exchange_ratio(from_currency: str, to_currency: str):
    return EXCHANGE_VS_EUR.get(from_currency, 1.0) * EXCHANGE_VS_EUR.get(to_currency, 1.0)


class Item(BaseModel):
    code: str


class Price(BaseModel):
    price: float
    currency: str


PRICES = {
    "diamond": Price(price=10000.01, currency="USD"),
    "rock": Price(price=123.45, currency="USD"),
    "paper": Price(price=33.33, currency="USD"),
    "scissors": Price(price=67.89, currency="JPY"),
}


def calculate_price(item_code: str) -> float:
    return PRICES[item_code]


class OrderDetail(BaseModel):
    item: str
    quantity: float


ORDERS = {
    1: [
        OrderDetail(item="rock", quantity=34),
        OrderDetail(item="scissors", quantity=72),
        OrderDetail(item="diamond", quantity=1)
    ],
    2: [
        OrderDetail(item="paper", quantity=23),
        OrderDetail(item="scissors", quantity=54),
        OrderDetail(item="rock", quantity=13)
    ]
}


def get_order(order_number: int) -> List[OrderDetail]:
    return ORDERS[order_number]
