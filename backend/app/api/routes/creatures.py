from typing import Annotated

from fastapi import APIRouter, Path

from app.api.deps import SessionDep
from app.core.config import settings
from app.enums import creatures_amount_map
from app.models import CreatureSummedStats, Stats, SummedStats, Unit,StageCounter

router = APIRouter(prefix="/creatures", tags=["creatures"])
BOSS_WAVES: list[int] = [5, 15, 21]


@router.get("/")
async def read_creatures(session: SessionDep) -> list[Unit]:
    creatures = (
        session.query(Unit)
        .filter(Unit.unit_class == "Creature")
        .order_by(Unit.sort_order)
        .all()
    )
    return creatures


def _read_creatures_by_stage(
    stage: Annotated[int, Path(ge=1, le=settings.STAGES_LIMIT)], session: SessionDep
) -> list[Unit]:
    creatures = (
        session.query(Unit)
        .filter(Unit.unit_class == "Creature")
        .filter(Unit.sort_order.startswith(f"creature_legion_id.{str(stage).zfill(2)}"))
        .all()
    )
    return creatures


@router.get("/{stage}")
async def read_creatures_by_stage(
    stage: Annotated[int, Path(ge=1, le=settings.STAGES_LIMIT)], session: SessionDep
) -> list[Unit]:
    creatures = _read_creatures_by_stage(stage=stage, session=session)
    return creatures


@router.get("/{stage}/stats")
async def calculate_stage_stats(
    stage: Annotated[int, Path(ge=1, le=settings.STAGES_LIMIT)], session: SessionDep
) -> CreatureSummedStats:
    creatures = _read_creatures_by_stage(stage=stage, session=session)

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

@router.post("/{stage}/counters")
async def sort_units_as_counters_by_stage(
    stage: Annotated[int, Path(ge=1, le=settings.STAGES_LIMIT)], units: list[Unit], session: SessionDep
) -> list[StageCounter]:
    creatures = _read_creatures_by_stage(stage=stage, session=session)
    counters = []
    for unit in units:
        unit_dict = unit.model_dump()
        counters.append(StageCounter(id=unit.id,hp_vs_stage=unit_dict.get(f"hp_vs_{creatures[0].attack_type.lower()}"), dps_vs_stage=unit_dict.get(f"dps_vs_{creatures[0].armor_type.lower()}"), gold_cost=unit.gold_cost))

    counters_sorted = sorted(counters, key= lambda counter:counter.dps_hp_value, reverse=True)
    return counters_sorted 



