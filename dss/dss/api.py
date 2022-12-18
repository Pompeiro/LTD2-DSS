from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from dss.dependencies import get_session

from .models import Hero

router = APIRouter(prefix="/dss", tags=["dss"])


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
