from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from dss.dependencies import get_session

from ..models import Arena

router = APIRouter(prefix="/{arena_id}", tags=["stats"])


@router.get("/")
async def sum_units_hp(
    arena_id: int, session: Session = Depends(get_session)
) -> list[Arena]:
    arena = session.get(Arena, arena_id)
    if not arena:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Arena with id: {arena_id} not found",
        )
    arena_units = arena.units
    unit_hps = []
    for unit in arena_units:
        unit_hps.append(unit.hp * arena.units_counter.get(unit.id))
    return sum(unit_hps)
