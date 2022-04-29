from typing import Optional
from fastapi import FastAPI
from base import Currency, Exchange, calculate_exchange_ratio

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/exchange", response_model=Exchange)
async def exchange(from_currency: Currency, to_currency: Currency):
    return Exchange(exchange_ratio=calculate_exchange_ratio(from_currency.code, to_currency.code))
