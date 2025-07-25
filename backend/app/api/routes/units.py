from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from app.api.deps import SessionDep
from app.models import LTD2Unit, Unit

router = APIRouter(prefix="/units", tags=["units"])


@router.post("/", status_code=HTTPStatus.CREATED)
async def clone_units_from_database(
    session: SessionDep,
) -> None:
    ltd2_units = session.exec(select(LTD2Unit)).all()
    units = [Unit(**unit.model_dump()) for unit in ltd2_units]
    try:
        session.bulk_save_objects(units)
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Attempt to add units with the same id, database already populated",
        )
    session.commit()
    session.expire_all()


@router.get("/")
async def read_units(
    session: SessionDep, offset: int = 0, limit: int = Query(default=10, le=500)
) -> list[Unit]:
    units = session.exec(select(Unit).offset(offset).limit(limit)).all()
    return units


@router.get("/element")
async def read_element_units(session: SessionDep) -> list[Unit]:
    units = (
        session.query(Unit)
        .filter(Unit.legion_id.startswith("element"))
        .filter(Unit.info_tier != None)  # noqa: E711
        .all()
    )
    base_units = filter(lambda unit: unit.upgrades_from == [], units)
    return base_units


@router.get("/{name}")
async def read_unit(name: str, session: SessionDep) -> Unit:
    unit = session.query(Unit).filter(Unit.name == name.title()).first()
    if not unit:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=f"Unit with name: {name} not found"
        )
    return unit
