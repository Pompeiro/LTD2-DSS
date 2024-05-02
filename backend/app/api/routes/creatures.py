from fastapi import APIRouter

from app.api.deps import SessionDep
from app.enums import creatures_amount_map
from app.models import Stats, Unit

router = APIRouter()


@router.get("/creatures")
async def read_creatures(session: SessionDep) -> list[Unit]:
    creatures = (
        session.query(Unit)
        .filter(Unit.unit_class == "Creature")
        .order_by(Unit.sort_order)
        .all()
    )
    return creatures


@router.get("/creatures/{stage}")
async def read_creatures_by_stage(stage: int, session: SessionDep) -> list[Unit]:
    stage = str(stage).zfill(2)
    creatures = (
        session.query(Unit)
        .filter(Unit.unit_class == "Creature")
        .filter(Unit.sort_order.startswith(f"creature_legion_id.{stage}"))
        .all()
    )
    return creatures


@router.get("/creatures/{stage}/calculate-wave")
async def calculate_wave_stats(stage: int, session: SessionDep) -> Stats:
    stage = str(stage).zfill(2)
    creatures = (
        session.query(Unit)
        .filter(Unit.unit_class == "Creature")
        .filter(Unit.sort_order.startswith(f"creature_legion_id.{stage}"))
        .all()
    )
    stats = Stats()
    stat_items = stats.dict().keys()
    for stats_item in stat_items:
        units_stat = []
        for creature in creatures:
            units_stat.append(
                getattr(creature, stats_item) * creatures_amount_map.get(creature.name)
            )
        setattr(stats, stats_item, sum(units_stat))
    return stats
