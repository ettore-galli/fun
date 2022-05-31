# https://towardsdatascience.com/why-you-should-use-async-in-python-6ab53740077e
# http://zderadicka.eu/functional-fun-with-asyncio-and-monads/

from __future__ import annotations
from concurrent.futures import Future
from sre_constants import SUCCESS

from typing import Any, Callable, Coroutine, Iterator, List, Optional
import aiohttp
import asyncio
import re


WEBSITES = ["http://www.html.it",
            "http://www.arcocer.it", "http://www.arcimm.it"]


async def get_session():
    return aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))


async def http_get(session: aiohttp.ClientSession, url: str) -> Coroutine:
    async with session.get(url) as response:
        resp = await response.text()
        return resp


def clean_data(data: str):
    return re.sub(r"[\n\r ]", "", data)


async def store_results(result):
    print("*" * 78)
    print(clean_data(result)[:78])
    print("*" * 78)


# --------------------------------------------------------------------------------


class Workflow:
    def __init__(
        self,
        result: Optional[Any] = None,
        success: Optional[bool] = None,
        message: Optional[str] = None,
    ) -> None:
        self.result = result
        self.success = success
        self.message = message

    @classmethod
    def unit(
        cls,
        result: Optional[Any] = None,
        success: Optional[bool] = None,
        message: Optional[str] = None,
    ):
        return Workflow(result=result, success=success, message=message)

    def bind(self, f: Callable[[Any], Workflow]):
        async def _bind():
            result: Workflow = await f(
                await self.result()
                if isinstance(self.result, Callable)
                else self.result
            )
            return result.result

        return Workflow(result=_bind)

    def __rshift__(self, other):
        return self.bind(other)


async def process_one(session, url):
    async def fetch_data(url) -> Workflow:
        return Workflow(result=await http_get(session, url))

    async def log_data(data) -> Workflow:
        print(f"Logging data {clean_data(str(data))[:30]}")
        return Workflow(result=data)

    async def save_data(data) -> Workflow:
        return Workflow(result=await store_results(data))

    bind_syntax: bool = True
    if bind_syntax:
        return (
            await Workflow.unit(url)
            .bind(fetch_data)
            .bind(log_data)
            .bind(save_data)
            .result()
        )

    shift_syntax: bool = True
    if shift_syntax:
        workflow = Workflow.unit(url) >> fetch_data >> log_data >> save_data
        return await (workflow).result()


async def process_all():
    http_session = await get_session()
    async with http_session as session:
        await process_one(session, WEBSITES[0])


def workflow():
    asyncio.run(process_all())


if __name__ == "__main__":
    workflow()
