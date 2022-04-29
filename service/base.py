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
