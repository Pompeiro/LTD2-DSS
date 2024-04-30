from collections import Counter
from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.api.deps import SessionDep
from app.models import Arena, CreateUpdateArena, Unit

router = APIRouter()


@router.post("/", status_code=HTTPStatus.CREATED)
async def create_arena(arena: CreateUpdateArena, session: SessionDep) -> Arena:
    current_arena = session.get(Arena, arena.id)
    if current_arena:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=f"Arena with id {current_arena.id} already exists",
        )

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
async def read_arenas(session: SessionDep) -> list[Arena]:
    arenas = session.exec(select(Arena)).all()
    return arenas


@router.put("/{arena_id}")
async def update_arena(
    *, arena_id: int, units: list[str], clear_units: bool = False, session: SessionDep
) -> Arena:
    db_arena = session.get(Arena, arena_id)
    if not db_arena:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Arena with id: {arena_id} not found",
        )
    if clear_units is True:
        db_arena.units_counter.clear()
        db_arena.units.clear()
    for unit in units:
        db_arena.units.append(  # pylint: disable=no-member
            session.exec(select(Unit).where(Unit.id == unit)).one()
        )
    unit_ids = [unit.id for unit in db_arena.units[-(len(units)) :]]
    db_arena.units_counter = Counter(db_arena.units_counter)
    db_arena.units_counter.update(unit_ids)
    session.add(db_arena)
    session.commit()
    session.refresh(db_arena)
    return db_arena


@router.get("/{arena_id}")
async def read_arena(arena_id: int, session: SessionDep) -> Arena:
    arena = session.get(Arena, arena_id)
    if not arena:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Arena with id: {arena_id} not found",
        )
    return arena
