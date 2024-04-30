from collections.abc import Sequence
from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from app.api.deps import SessionDep
from app.models import LTD2Unit, Unit

router = APIRouter()


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
) -> Sequence[Unit]:
    units = session.exec(select(Unit).offset(offset).limit(limit)).all()
    return units


@router.get("/{name}")
async def read_unit(name: str, session: SessionDep) -> Unit:
    unit = session.query(Unit).filter(Unit.name == name.title()).first()
    if not unit:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=f"Unit with name: {name} not found"
        )
    return unit
