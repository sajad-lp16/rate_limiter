import asyncio

from requests.functions import request_generator
from provider_service import Provider
from utils.router import Router
from utils.user_prompt import load_config


async def main():
    config = load_config()
    router = Router

    providers_names = list(config.keys())
    for key, value in config.items():
        provider = Provider(identifier=key, **value)
        router.register(route=key, provider=provider)

    await asyncio.create_task(request_generator(providers_names))
    await asyncio.sleep(50)


if __name__ == '__main__':
    asyncio.run(main())
