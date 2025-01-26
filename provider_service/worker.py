import asyncio
from typing import TYPE_CHECKING
from asyncio import PriorityQueue
from datetime import datetime

from provider_service.base import BaseProvider
from requests.controller import RequestController
from requests import (
    Request,
    Headers,
    post_request
)
from utils.validators import (
    is_valid_url,
    is_valid_rate_limit,
    is_string_key_value_dict,
)

if TYPE_CHECKING:
    from provider_service import Provider


class ProviderWorker(BaseProvider):
    """
    handles communication responsibility.
    queues requests submitted by associated provider, and processes them when the provider is active.

    this class respects request priority and execution time of each request.
    """
    def __init__(
            self,
            api_endpoint: str,
            headers: Headers[str, str],
            rate_limit: int | float,
            provider: "Provider",
    ) -> None:

        field_2_validator = {
            api_endpoint: is_valid_url,
            headers: is_string_key_value_dict,
            rate_limit: is_valid_rate_limit,
        }
        self.validate_fields(field_2_validator)

        self.api_endpoint = api_endpoint
        self.headers = headers
        self.request_controller = RequestController(rate_limit)
        self.provider = provider
        self._requests_queue = PriorityQueue(maxsize=100_000)
        self._is_active = True

    def run(self) -> None:
        self._is_active = True
        asyncio.create_task(self.spawn_request_processors())

    def stop(self) -> None:
        self._is_active = False

    async def perform_request(self, request: Request) -> None:
        if self._requests_queue.full():
            print(f"requests queue of {self.provider} is full please this might take a few seconds")

        await self.insert_to_queue(request)

    async def spawn_request_processors(self) -> None:
        while self._is_active:
            if self.request_controller.is_locked:
                suspend_delay = self.request_controller.get_suspend_time()
                await asyncio.sleep(suspend_delay)
                continue
            request = await self._requests_queue.get()
            _ = asyncio.create_task(self.process_request(request))

    async def process_request(self, request: Request) -> None:
        if request.execution_time is not None:
            if not request.execution_time <= datetime.now():
                execution_delay = (request.execution_time - datetime.now()).total_seconds()
                print(
                    f"request={request} for {self.provider} has scheduled and will start in {execution_delay} seconds")
                await asyncio.sleep(execution_delay)

        while not self.request_controller.request_is_allowed():
            suspend_delay = self.request_controller.get_suspend_time()
            await asyncio.sleep(suspend_delay)

        self._requests_queue.task_done()

        if not self._is_active:
            await self.insert_to_queue(request)
            return

        process_delay = await post_request(self.api_endpoint, self.headers, request)

        print(f"request={request} has been successfully done by {self.provider} in {process_delay} seconds")

    async def insert_to_queue(self, request: Request) -> None:
        insertion_task = asyncio.create_task(self._requests_queue.put(request))
        try:
            await asyncio.wait_for(asyncio.shield(insertion_task), timeout=10)
        except asyncio.TimeoutError:
            print(f"request queue insertion for {self.provider} is taking too long, possible issues:\n"
                  f"1) request generator is way faster than provider consumption\n"
                  f"2) the provider is suspended for a long time\n"
                  f"any way the task is not canceled but it might take very long!")
            await insertion_task

    def __str__(self) -> str:
        return f"{self.provider}'s worker, state={self._is_active}, tasks_in_queue={self._requests_queue.qsize()}"

    def __repr__(self) -> str:
        return (f"ProviderWorker(provider={self.provider}, state={self._is_active},"
                f" tasks_in_queue={self._requests_queue.qsize()}")
