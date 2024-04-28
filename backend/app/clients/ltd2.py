from collections.abc import AsyncGenerator

from playwright.async_api import APIRequestContext, async_playwright

from app.core.config import settings
from app.models import LTD2UnitFromAPI

assert settings.LTD2_X_API_KEY, "LTD2 X API KEY not set"


async def get_api_request_context() -> AsyncGenerator[APIRequestContext, None]:
    async with async_playwright() as playwright:
        headers = {
            "x-api-key": settings.LTD2_X_API_KEY,
        }
        request_context = await playwright.request.new_context(
            base_url="https://apiv2.legiontd2.com", extra_http_headers=headers
        )
        yield request_context


async def find_unit_by_name(name: str, api_request_context: APIRequestContext) -> dict:  # type:ignore
    unit = await api_request_context.get(f"/units/byName/{name}")
    unit_response = await unit.json()
    return unit_response  # type:ignore


async def get_current_game_version(api_request_context: APIRequestContext) -> str:
    unit_response = await find_unit_by_name(
        name="Berserker", api_request_context=api_request_context
    )
    version = unit_response["version"]
    return version  # type:ignore


async def find_units_by_version(
    version: str, api_request_context: APIRequestContext
) -> list[LTD2UnitFromAPI]:
    units = await api_request_context.get(
        f"/units/byVersion/{version}", params={"limit": 250}
    )
    units_response = await units.json()
    if len(units_response) == 250:
        units_remaining = await api_request_context.get(
            f"/units/byVersion/{version}", params={"limit": 250, "offset": 250}
        )
        units_remaining_response = await units_remaining.json()
        units_response = units_response + units_remaining_response

    return [
        LTD2UnitFromAPI.model_validate(LTD2UnitFromAPI(**unit))
        for unit in units_response
    ]
