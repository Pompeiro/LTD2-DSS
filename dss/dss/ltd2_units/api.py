from http import HTTPStatus

from fastapi import APIRouter, Depends
from playwright.async_api import APIRequestContext
from sqlmodel import Session, select

from dss.clients.ltd2 import (
    find_units_by_version,
    get_api_request_context,
    get_current_game_version,
)
from dss.dependencies import get_session

from .models import LTD2Unit

router = APIRouter(prefix="/ltd2-units", tags=["ltd2-units"])


@router.post("/", status_code=HTTPStatus.CREATED)
async def clone_units_from_ltd2_api(
    session: Session = Depends(get_session),
    api_request_context: APIRequestContext = Depends(get_api_request_context),
) -> None:
    version = await get_current_game_version(api_request_context=api_request_context)
    units_list = await find_units_by_version(
        version=version, api_request_context=api_request_context
    )
    units = [LTD2Unit(**unit) for unit in units_list]
    session.bulk_save_objects(units)
    session.commit()
    session.expire_all()


@router.get("/")
async def read_units(session: Session = Depends(get_session)) -> list[LTD2Unit]:
    units = session.exec(select(LTD2Unit)).all()
    return units
