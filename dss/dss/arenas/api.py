from collections import Counter
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from dss.dependencies import get_session

from ..units import Unit
from .models import Arena, CreateUpdateArena
from .stats import stats_router

router = APIRouter(prefix="/arenas", tags=["arenas"])
router.include_router(stats_router)


@router.post("/", status_code=HTTPStatus.CREATED)
async def create_arena(
    arena: CreateUpdateArena,
    session: Session = Depends(get_session),
) -> Arena:
    db_arena = Arena(id=arena.id, units=[])
    for unit_id in arena.unit_ids:
        db_arena.units.append(  # pylint: disable=no-member
            session.exec(select(Unit).where(Unit.id == unit_id)).one()
        )
    db_arena.units_counter = Counter(db_arena.units_counter)
    db_arena.units_counter.update(arena.unit_ids)
    session.add(db_arena)
    session.commit()
    session.refresh(db_arena)
    return db_arena


@router.get("/")
async def read_arenas(session: Session = Depends(get_session)) -> list[Arena]:
    arenas = session.exec(select(Arena)).all()
    return arenas


@router.get("/{arena_id}")
async def read_arena(arena_id: int, session: Session = Depends(get_session)) -> Arena:
    arena = session.get(Arena, arena_id)
    if not arena:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Arena with id: {arena_id} not found",
        )
    return arena
