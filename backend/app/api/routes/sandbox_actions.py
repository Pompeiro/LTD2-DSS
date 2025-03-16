from pathlib import Path

from fastapi import APIRouter, Response

from app.localstack.sandbox_actions import (
    check_wave_indicator,
    fill_whole_grid_with_towers,
    ocr_event_history_log,
    place_towers_flow,
)

STATIC_IMAGES_SANDBOX_DIR = Path("app/images/static/sandbox")


router = APIRouter(prefix="/sandbox-action", tags=["sandbox-action"])


@router.get("/fill-grid")
async def fill_whole_grid_with_towers_() -> Response:
    return fill_whole_grid_with_towers()


@router.get("/place-towers-flow")
async def place_towers_flow_(tower_position: int, tower_amount: int) -> list[str]:
    return place_towers_flow(tower_position=tower_position, tower_amount=tower_amount)


@router.get("/check-wave-indicator")
async def check_wave_indicator_() -> bool:
    return check_wave_indicator()


@router.get("/ocr-event-history-log")
async def ocr_event_history_log_() -> list[str]:
    return ocr_event_history_log()
