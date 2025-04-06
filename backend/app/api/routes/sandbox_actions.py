from pathlib import Path

from fastapi import APIRouter, Response

from app.localstack.sandbox_actions import (
    check_wave_indicator,
    fill_whole_grid_with_towers,
)

STATIC_IMAGES_SANDBOX_DIR = Path("app/images/static/sandbox")


router = APIRouter(prefix="/sandbox-action", tags=["sandbox-action"])


@router.get("/fill-grid")
async def fill_whole_grid_with_towers_() -> Response:
    return fill_whole_grid_with_towers()


@router.get("/check-wave-indicator")
async def check_wave_indicator_() -> bool:
    return check_wave_indicator()
