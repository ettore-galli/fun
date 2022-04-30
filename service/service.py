from typing import Optional
from fastapi import FastAPI
from base import Currency, Exchange, calculate_exchange_ratio, Item,  Price, calculate_price, OrderDetail, get_order

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/orders/{order_number}")
async def exchange(order_number: int):
    print(order_number)
    return get_order(order_number=order_number)


@app.post("/exchange", response_model=Exchange)
async def exchange(from_currency: Currency, to_currency: Currency):
    return Exchange(exchange_ratio=calculate_exchange_ratio(from_currency.code, to_currency.code))


@app.post("/price", response_model=Price)
async def exchange(item: Item):
    return calculate_price(item.code)
