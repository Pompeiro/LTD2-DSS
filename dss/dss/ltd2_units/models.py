from typing import Optional

from sqlmodel import Field, SQLModel


class LTD2Unit(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True, alias="_id")
    unit_id: str = Field(alias="unitId")
    version: str
    abilities: list[str]
    armor_type: str = Field(alias="armorType")
    aspd_inverted: Optional[float] = Field(default=None, alias="aspdInverted")
    attack_mode: str = Field(alias="attackMode")
    attack_range: Optional[int] = Field(default=None, alias="attackRange")
    attack_speed: Optional[float] = Field(default=None, alias="attackSpeed")
    attack_type: str = Field(alias="attackType")
    avg_aspd: float = Field(alias="avgAspd")
    avg_aspd_diff: float = Field(alias="avgAspdDiff")
    avg_cost: float = Field(alias="avgCost")
    avg_cost_diff: float = Field(alias="avgCostDiff")
    avg_dmg: float = Field(alias="avgDmg")
    avg_dmg_diff: float = Field(alias="avgDmgDiff")
    avg_hp: float = Field(alias="avgHp")
    avg_hp_diff: float = Field(alias="avgHpDiff")
    avg_mspd: float = Field(alias="avgMspd")
    avg_mspd_diff: float = Field(alias="avgMspdDiff")
    category_class: str = Field(alias="categoryClass")
    description: str
    description_id: str = Field(alias="descriptionId")
    dmg_base: Optional[int] = Field(default=None, alias="dmgBase")
    dmg_expected: Optional[float] = Field(default=None, alias="dmgExpected")
    dmg_max: Optional[int] = Field(default=None, alias="dmgMax")
    dps: Optional[float] = Field(default=None)
    flags: str
    gold_bounty: Optional[int] = Field(default=None, alias="goldBounty")
    gold_cost: Optional[int] = Field(default=None, alias="goldCost")
    gold_value: Optional[int] = Field(default=None, alias="goldValue")
    hp: int
    icon_path: str = Field(alias="iconPath")
    income_bonus: Optional[int] = Field(default=None, alias="incomeBonus")
    info_sketchfab: Optional[str] = Field(default=None, alias="infoSketchfab")
    info_tier: str = Field(alias="infoTier")
    is_enabled: bool = Field(alias="isEnabled")
    legion_id: str = Field(alias="legionId")
    model_scale: float = Field(alias="modelScale")
    move_speed: Optional[int] = Field(default=None, alias="moveSpeed")
    move_type: str = Field(alias="moveType")
    mp: Optional[int] = Field(default=None)
    mspd_text: str = Field(alias="mspdText")
    mythium_cost: Optional[int] = Field(default=None, alias="mythiumCost")
    name: str
    radius: str
    range_text: str = Field(alias="rangeText")
    sort_order: str = Field(alias="sortOrder")
    splash_path: str = Field(alias="splashPath")
    stock_max: Optional[int] = Field(default=None, alias="stockMax")
    stock_time: Optional[int] = Field(default=None, alias="stockTime")
    tooltip: str
    total_value: Optional[int] = Field(default=None, alias="totalValue")
    unit_class: str = Field(alias="unitClass")
    upgrades_from: list[str] = Field(alias="upgradesFrom")
