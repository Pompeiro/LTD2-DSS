from typing import AsyncGenerator

from playwright.async_api import APIRequestContext, async_playwright

from dss.settings import settings

assert settings.ltd2_x_api_key, "LTD2 X API KEY not set"


async def get_api_request_context() -> AsyncGenerator[APIRequestContext, None]:
    async with async_playwright() as playwright:
        headers = {
            "x-api-key": settings.ltd2_x_api_key,
        }
        request_context = await playwright.request.new_context(
            base_url="https://apiv2.legiontd2.com", extra_http_headers=headers
        )
        yield request_context


async def find_unit_by_name(name: str, api_request_context: APIRequestContext) -> dict:
    unit = await api_request_context.get(f"/units/byName/{name}")
    unit_response = await unit.json()
    return unit_response


async def get_current_game_version(api_request_context: APIRequestContext) -> str:
    unit_response = await find_unit_by_name(
        name="Berserker", api_request_context=api_request_context
    )
    version = unit_response["version"]
    return version


async def find_units_by_version(
    version: str, api_request_context: APIRequestContext
) -> dict:
    units = await api_request_context.get(
        f"/units/byVersion/{version}", params={"limit": 250}
    )
    units_response = await units.json()
    return units_response
