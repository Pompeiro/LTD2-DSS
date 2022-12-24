from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from dss.dependencies import get_session

from .ltd2_units import ltd2_units_router
from .models import Hero
from .units import units_router

router = APIRouter(prefix="/dss", tags=["dss"])
router.include_router(ltd2_units_router)
router.include_router(units_router)


@router.post("/heroes")
def create_hero(hero: Hero, session: Session = Depends(get_session)) -> Hero:
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


@router.get("/heroes")
def read_heroes(session: Session = Depends(get_session)) -> list[Hero]:
    heroes = session.exec(select(Hero)).all()
    return heroes
