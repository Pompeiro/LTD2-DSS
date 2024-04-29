from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from app.api.deps import SessionDep
from app.models import Arena, Stats

router = APIRouter()


@router.get("/")
async def sum_units_hp(arena_id: int, session: SessionDep) -> Stats:
    arena = session.get(Arena, arena_id)
    if not arena:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Arena with id: {arena_id} not found",
        )
    stats = Stats()
    stat_items = stats.dict().keys()
    for stats_item in stat_items:
        units_stat = []
        for unit in arena.units:
            units_stat.append(
                getattr(unit, stats_item) * arena.units_counter.get(unit.id)
            )
        setattr(stats, stats_item, sum(units_stat))
    return stats
