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

@router.get("/{stage}/counter")
async def read_counter_by_stage(
    stage: Annotated[int, Path(ge=1, le=settings.STAGES_LIMIT)], session: SessionDep
) -> StageCounter:
    units = [Unit(id="proton_unit_id", name="Proton", sort_order="element_legion_id.T1.20.Proton", hp=130, armor_type="Immaterial", mp=None, move_speed=300, move_type="Air", attack_range=300, attack_speed=0.845, attack_type="Pure", dmg_base=12, dps=14.2, gold_cost=20, total_value=20, flags="flags_flying", info_tier="Tier-1", is_enabled=True, legion_id="element_legion_id", unit_class="Fighter", icon_path="Icons/Proton.png", splash_path="Splashes/Proton.png", version="12.02.3", upgrades_from=[], arena_id=None, hp_vs_impact=130.0, hp_vs_pierce=130.0, hp_vs_magic=130.0, hp_vs_pure=130.0, dps_vs_swift=14.2, dps_vs_natural=14.2, dps_vs_fortified=14.2, dps_vs_arcane=14.2, dps_vs_immaterial=14.2), Unit(id="aqua_spirit_unit_id", name="Aqua Spirit", sort_order="element_legion_id.T2.50.Aqua Spirit", hp=370, armor_type="Arcane", mp=None, move_speed=300, move_type="Ground", attack_range=400, attack_speed=1.2, attack_type="Pierce", dmg_base=24, dps=20.0, gold_cost=50, total_value=50, flags="flags_ground", info_tier="Tier-2", is_enabled=True, legion_id="element_legion_id", unit_class="Fighter", icon_path="Icons/AquaSpirit.png", splash_path="Splashes/AquaSpirit.png", version="12.02.3", upgrades_from=[], arena_id=None, hp_vs_impact=321.7391304347826, hp_vs_pierce=321.7391304347826, hp_vs_magic=493.3333333333333, hp_vs_pure=370.0, dps_vs_swift=24.0, dps_vs_natural=17.0, dps_vs_fortified=16.0, dps_vs_arcane=23.0, dps_vs_immaterial=20.0), Unit(id="windhawk_unit_id", name="Windhawk", sort_order="element_legion_id.T3.85.Windhawk", hp=760, armor_type="Natural", mp=None, move_speed=300, move_type="Air", attack_range=100, attack_speed=0.82, attack_type="Impact", dmg_base=35, dps=42.68, gold_cost=85, total_value=85, flags="flags_flying", info_tier="Tier-3", is_enabled=True, legion_id="element_legion_id", unit_class="Fighter", icon_path="Icons/Windhawk.png", splash_path="Splashes/Windhawk.png", version="12.02.3", upgrades_from=[], arena_id=None, hp_vs_impact=844.4444444444445, hp_vs_pierce=894.1176470588235, hp_vs_magic=608.0, hp_vs_pure=760.0, dps_vs_swift=34.144, dps_vs_natural=38.412, dps_vs_fortified=49.081999999999994, dps_vs_arcane=49.081999999999994, dps_vs_immaterial=42.68), Unit(id="mudman_unit_id", name="Mudman", sort_order="element_legion_id.T4.140.Mudman", hp=1290,armor_type="Fortified", mp=None, move_speed=300, move_type="Ground", attack_range=100, attack_speed=1.35, attack_type="Impact", dmg_base=53, dps=39.26, gold_cost=140, total_value=140, flags="flags_ground", info_tier="Tier-4", is_enabled=True, legion_id="element_legion_id", unit_class="Fighter", icon_path="Icons/Mudman.png", splash_path="Splashes/Mudman.png", version="12.02.3", upgrades_from=[], arena_id=None, hp_vs_impact=1121.7391304347827, hp_vs_pierce=1612.5, hp_vs_magic=1228.5714285714284, hp_vs_pure=1290.0, dps_vs_swift=31.408, dps_vs_natural=35.333999999999996, dps_vs_fortified=45.148999999999994, dps_vs_arcane=45.148999999999994, dps_vs_immaterial=39.26), Unit(id="disciple_unit_id", name="Disciple", sort_order="element_legion_id.T5.195.Disciple", hp=1150, armor_type="Swift", mp=14, move_speed=300, move_type="Ground", attack_range=500, attack_speed=1.15, attack_type="Pierce", dmg_base=71, dps=61.74, gold_cost=195, total_value=195, flags="flags_ground,flags_organic", info_tier="Tier-5", is_enabled=True, legion_id="element_legion_id", unit_class="Fighter", icon_path="Icons/Disciple.png", splash_path="Splashes/Disciple.png", version="12.02.3", upgrades_from=[], arena_id=None, hp_vs_impact=1437.5, hp_vs_pierce=958.3333333333334, hp_vs_magic=1150.0, hp_vs_pure=1150.0, dps_vs_swift=74.088, dps_vs_natural=52.479, dps_vs_fortified=49.392, dps_vs_arcane=71.00099999999999, dps_vs_immaterial=61.74), Unit(id="fire_lord_unit_id", name="Fire Lord", sort_order="element_legion_id.T6.275.Fire Lord", hp=1780, armor_type="Swift", mp=8, move_speed=300, move_type="Ground", attack_range=200, attack_speed=0.95, attack_type="Magic", dmg_base=134, dps=141.05, gold_cost=275, total_value=275, flags="flags_ground", info_tier="Tier-6", is_enabled=True, legion_id="element_legion_id", unit_class="Fighter", icon_path="Icons/FireLord.png", splash_path="Splashes/FireLord.png", version="12.02.3", upgrades_from=[], arena_id=None, hp_vs_impact=2225.0, hp_vs_pierce=1483.3333333333335, hp_vs_magic=1780.0, hp_vs_pure=1780.0, dps_vs_swift=141.05, dps_vs_natural=176.3125, dps_vs_fortified=148.10250000000002, dps_vs_arcane=105.78750000000001, dps_vs_immaterial=141.05)]
    creatures = _read_creatures_by_stage(stage=stage, session=session)
    counters = []
    for unit in units:
        unit_dict = unit.model_dump()
        counters.append(StageCounter(id=unit.id,hp_vs_stage=unit_dict.get(f"hp_vs_{creatures[0].attack_type.lower()}"), dps_vs_stage=unit_dict.get(f"dps_vs_{creatures[0].armor_type.lower()}"), gold_cost=unit.gold_cost))

    counters_sorted = sorted(counters, key= lambda counter:counter.dps_hp_value, reverse=True)
    return counters_sorted 



