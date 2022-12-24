from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from dss.dependencies import get_session
from dss.dss.ltd2_units import LTD2Unit

from .models import Unit

router = APIRouter(prefix="/units", tags=["units"])


@router.post("/", status_code=HTTPStatus.CREATED)
async def clone_units_from_database(
    session: Session = Depends(get_session),
) -> None:
    ltd2_units = session.exec(select(LTD2Unit)).all()
    units = [Unit(**unit.dict()) for unit in ltd2_units]
    session.bulk_save_objects(units)
    session.commit()
    session.expire_all()


@router.get("/")
async def read_units(session: Session = Depends(get_session)) -> list[Unit]:
    units = session.exec(select(Unit)).all()
    return units


@router.get("/{name}")
async def read_unit(name: str, session: Session = Depends(get_session)) -> Unit:
    unit = session.query(Unit).filter(Unit.name == name.title()).first()
    if not unit:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=f"Unit with name: {name} not found"
        )
    return unit
