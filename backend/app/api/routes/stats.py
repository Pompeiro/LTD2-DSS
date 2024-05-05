from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Path

from app.api.deps import SessionDep
from app.api.routes.creatures import calculate_stage_stats
from app.core.config import settings
from app.enums import stage_armor_to_arena_dps_vs_map, stage_attack_to_arena_hp_vs_map
from app.models import Arena, ArenaStatsVsStage, CreatureSummedStats, Stats, SummedStats

router = APIRouter()


@router.get("/")
async def sum_units_stats(arena_id: int, session: SessionDep) -> SummedStats:
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
    summed_stats = SummedStats(**stats.model_dump())
    return summed_stats


@router.get("/{stage}/")
async def read_summed_arena_and_creatures_stats(
    *,
    arena_id: int,
    stage: Annotated[int, Path(ge=1, le=settings.STAGES_LIMIT)],
    session: SessionDep,
) -> tuple[SummedStats, CreatureSummedStats]:
    summed_stats = await sum_units_stats(arena_id=arena_id, session=session)
    stage_stats = await calculate_stage_stats(stage=stage, session=session)
    return (summed_stats, stage_stats)


@router.get("/{stage}/compare")
async def compare_arena_vs_stage_stats(
    *,
    arena_id: int,
    stage: Annotated[int, Path(ge=1, le=settings.STAGES_LIMIT)],
    session: SessionDep,
) -> ArenaStatsVsStage:
    summed_stats = await sum_units_stats(arena_id=arena_id, session=session)
    stage_stats = await calculate_stage_stats(stage=stage, session=session)

    arena_stats_vs_stage_create = ArenaStatsVsStage.model_construct()
    arena_stats_vs_stage_create.arena_hp_vs_stage_attack_type = getattr(
        summed_stats, stage_attack_to_arena_hp_vs_map.get(stage_stats.attack_type)
    )
    arena_stats_vs_stage_create.arena_dps_vs_stage_armor_type = getattr(
        summed_stats, stage_armor_to_arena_dps_vs_map.get(stage_stats.armor_type)
    )
    arena_stats_vs_stage_create.stage_armor_type = stage_stats.armor_type
    arena_stats_vs_stage_create.stage_attack_type = stage_stats.attack_type
    arena_stats_vs_stage_create.stage_hp = stage_stats.hp
    arena_stats_vs_stage_create.stage_dps = stage_stats.dps
    arena_stats_vs_stage = ArenaStatsVsStage(**arena_stats_vs_stage_create.model_dump())

    return arena_stats_vs_stage
