import random
import secrets
import asyncio

from requests import (
    Request,
    Headers
)


async def request_generator(routing_list: list[str]):
    from utils.router import Router

    print("Starting Request Generator . . .\n\n\n")

    id_ = 1
    router = Router

    while True:
        for _ in range(100):
            message = f"uid={id_}_{secrets.token_urlsafe(10)}"
            priority = random.randint(1, 5)
            request = Request(priority=priority, message=message)
            target_provider = random.choice(routing_list)

            router.forward_request(target_provider, request)
            id_ += 1
        await asyncio.sleep(1)


async def post_request(url: str, headers: Headers, request: Request):
    _ = headers

    payload = {"data": request.message}
    print(f"requesting {url} for {request} ...")

    delay = random.random() * 2
    await asyncio.sleep(delay)  # simulate processing daley
    return delay
