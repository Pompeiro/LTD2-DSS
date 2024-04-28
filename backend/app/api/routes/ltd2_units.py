from collections.abc import Sequence
from http import HTTPStatus

from fastapi import APIRouter, Query
from sqlmodel import select

from app.api.deps import APIRequestContextDep, SessionDep
from app.clients.ltd2 import (
    find_units_by_version,
    get_current_game_version,
)
from app.models import LTD2Unit

router = APIRouter()


@router.post("/", status_code=HTTPStatus.CREATED)
async def clone_units_from_ltd2_api(
    session: SessionDep,
    api_request_context: APIRequestContextDep,
) -> None:
    version = await get_current_game_version(api_request_context=api_request_context)
    units_list = await find_units_by_version(
        version=version, api_request_context=api_request_context
    )
    ltd2_units = [LTD2Unit.model_validate(unit) for unit in units_list]

    session.bulk_save_objects(ltd2_units)
    session.commit()
    session.expire_all()


@router.get("/")
async def read_units(
    session: SessionDep, offset: int = 0, limit: int = Query(default=10, le=500)
) -> Sequence[LTD2Unit]:
    units = session.exec(select(LTD2Unit).offset(offset).limit(limit)).all()
    return units
