import asyncio

from requests import Request
from provider_service import Provider


class Router:
    ROUTE_2_PROVIDER_MAPPING = {}

    @classmethod
    def register(cls, route: str, provider: Provider):
        assert isinstance(provider, Provider) and isinstance(route, str), "invalid registration input"

        cls.ROUTE_2_PROVIDER_MAPPING[route] = provider

    @classmethod
    def forward_request(cls, route: str, request: Request):
        if (provider := cls.ROUTE_2_PROVIDER_MAPPING.get(route)) is None:
            print("wrong route")
            return False

        asyncio.create_task(provider.perform_request(request))
