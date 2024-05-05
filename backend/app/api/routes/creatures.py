from fastapi import APIRouter

from app.api.deps import SessionDep
from app.enums import creatures_amount_map
from app.models import CreatureSummedStats, Stats, SummedStats, Unit

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


@router.get("/creatures/{stage}/stats")
async def calculate_stage_stats(stage: int, session: SessionDep) -> CreatureSummedStats:
    stage = str(stage).zfill(2)
    creatures: list[Unit] = (
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
    summed_stats = SummedStats(**stats.model_dump())
    creature_stats = CreatureSummedStats(
        **summed_stats.model_dump(),
        attack_type=creatures[0].attack_type,
        armor_type=creatures[0].armor_type,
    )
    return creature_stats
