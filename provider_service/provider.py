import asyncio
import random

from provider_service.base import BaseProvider
from requests import (
    Request,
    Headers
)
from utils.validators import (
    is_valid_url,
    is_valid_rate_limit,
    is_non_blank_string,
    is_string_key_value_dict
)


class Provider(BaseProvider):
    """
    Provider class is the target for incoming requests after Router.
    provider passes requests to worker.
    when the provider is switched off, it will still accept requests, but they won't be processed by worker
    unless it (provider) starts again.
    """

    def __init__(self, identifier: str, api_endpoint: str, headers: dict[str, str], rate_limit: int | float) -> None:
        from provider_service import ProviderWorker

        headers = Headers(headers)  # make headers hashable

        field_2_validator = {
            identifier: is_non_blank_string,
            api_endpoint: is_valid_url,
            headers: is_string_key_value_dict,
            rate_limit: is_valid_rate_limit,
        }
        self.validate_fields(field_2_validator)

        self.identifier = identifier
        self.api_endpoint = api_endpoint
        self.headers = headers
        self.rate_limit = rate_limit
        self._is_active = True

        self.worker = ProviderWorker(api_endpoint=api_endpoint, headers=headers, rate_limit=rate_limit, provider=self)
        self.worker.run()

        asyncio.create_task(self.toggle_status())

    async def toggle_status(self) -> None:
        while True:
            sleep_time = random.randint(1, 2)
            await asyncio.sleep(0)

            self._is_active = not self._is_active
            self.worker.run() if self._is_active else self.worker.stop()

    async def perform_request(self, request: Request) -> None:
        if not self._is_active:
            print(f"{self.identifier} provider is not active at the moment but {request} is scheduled to run later")
        await self.worker.perform_request(request)

    def __str__(self) -> str:
        return f"{self.identifier}"

    def __repr__(self) -> str:
        return (f"Provider(identifier={self.identifier}, api={self.api_endpoint},"
                f" headers={self.headers}), rate_limit={self.rate_limit}")
