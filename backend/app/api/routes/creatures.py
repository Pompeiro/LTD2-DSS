from typing import Annotated

from fastapi import APIRouter, Path

from app.api.deps import SessionDep
from app.core.config import settings
from app.enums import creatures_amount_map
from app.models import CreatureSummedStats, Stats, SummedStats, Unit

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


def handle_stage_number_considering_boss_waves(stage: int) -> int:
    for boss_wave in BOSS_WAVES:
        if stage > boss_wave:
            stage = stage + 1
    return stage


def _read_creatures_by_stage(
    stage: Annotated[int, Path(ge=1, le=settings.STAGES_LIMIT)], session: SessionDep
) -> list[Unit]:
    stage_modified = handle_stage_number_considering_boss_waves(stage=stage)
    creatures = []
    creatures.append(
        session.query(Unit)
        .filter(Unit.unit_class == "Creature")
        .filter(
            Unit.sort_order.startswith(
                f"creature_legion_id.{str(stage_modified).zfill(2)}"
            )
        )
        .all()
    )
    if stage_modified in BOSS_WAVES:
        creatures.append(
            session.query(Unit)
            .filter(Unit.unit_class == "Creature")
            .filter(
                Unit.sort_order.startswith(
                    f"creature_legion_id.{str(stage_modified+1).zfill(2)}"
                )
            )
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
