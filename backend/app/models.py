import uuid
from typing import Optional

from pydantic import EmailStr, computed_field, field_validator
from sqlmodel import JSON, Column, Field, Relationship, SQLModel

from .enums import ArmorTypes, AttackTypes, damage_def_map


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


class LTD2UnitFromAPI(SQLModel, table=True):
    id: str = Field(alias="_id")
    unit_id: str = Field(default=None, primary_key=True, alias="unitId")
    version: str
    abilities: list[str] = Field(sa_column=Column(JSON))
    armor_type: str | None = Field(default=None, alias="armorType")
    aspd_inverted: str | None = Field(default=None, alias="aspdInverted")
    attack_mode: str | None = Field(default=None, alias="attackMode")
    attack_range: str | None = Field(default=None, alias="attackRange")
    attack_speed: str | None = Field(default=None, alias="attackSpeed")
    attack_type: str | None = Field(default=None, alias="attackType")
    avg_aspd: str = Field(alias="avgAspd")
    avg_aspd_diff: str = Field(alias="avgAspdDiff")
    avg_cost: str = Field(alias="avgCost")
    avg_cost_diff: str = Field(alias="avgCostDiff")
    avg_dmg: str = Field(alias="avgDmg")
    avg_dmg_diff: str = Field(alias="avgDmgDiff")
    avg_hp: str = Field(alias="avgHp")
    avg_hp_diff: str = Field(alias="avgHpDiff")
    avg_mspd: str = Field(alias="avgMspd")
    avg_mspd_diff: str = Field(alias="avgMspdDiff")
    category_class: str = Field(alias="categoryClass")
    description: str
    description_id: str = Field(alias="descriptionId")
    dmg_base: str | None = Field(default=None, alias="dmgBase")
    dmg_expected: str | None = Field(default=None, alias="dmgExpected")
    dmg_max: str | None = Field(default=None, alias="dmgMax")
    dps: str | None = Field(default=None)
    flags: str
    gold_bounty: str | None = Field(default=None, alias="goldBounty")
    gold_cost: str | None = Field(default=None, alias="goldCost")
    gold_value: str | None = Field(default=None, alias="goldValue")
    hp: str
    icon_path: str = Field(alias="iconPath")
    income_bonus: str | None = Field(default=None, alias="incomeBonus")
    info_sketchfab: str | None = Field(default=None, alias="infoSketchfab")
    info_tier: str | None = Field(default=None, alias="infoTier")
    is_enabled: bool = Field(alias="isEnabled")
    legion_id: str = Field(alias="legionId")
    model_scale: str = Field(alias="modelScale")
    move_speed: str | None = Field(default=None, alias="moveSpeed")
    move_type: str | None = Field(default=None, alias="moveType")
    mp: str | None = Field(default=None)
    mspd_text: str = Field(alias="mspdText")
    mythium_cost: str | None = Field(default=None, alias="mythiumCost")
    name: str
    radius: str
    range_text: str = Field(alias="rangeText")
    sort_order: str = Field(alias="sortOrder")
    splash_path: str = Field(alias="splashPath")
    stock_max: str | None = Field(default=None, alias="stockMax")
    stock_time: str | None = Field(default=None, alias="stockTime")
    tooltip: str
    total_value: str | None = Field(default=None, alias="totalValue")
    unit_class: str = Field(alias="unitClass")
    upgrades_from: list[str] = Field(alias="upgradesFrom", sa_column=Column(JSON))

    @field_validator("*")
    @classmethod
    def set_empty_strings_to_none(cls, v: str | None) -> str | None:
        if v == "":
            v = None
        return v

    class Config:
        arbitrary_types_allowed = True


class LTD2Unit(SQLModel, table=True):
    id: str
    unit_id: str = Field(default=None, primary_key=True)
    version: str
    abilities: list[str] = Field(sa_column=Column(JSON))
    armor_type: str | None = None
    aspd_inverted: float | None = None
    attack_mode: str | None = None
    attack_range: int | None = None
    attack_speed: float | None = None
    attack_type: str | None = None
    avg_aspd: float
    avg_aspd_diff: float
    avg_cost: float
    avg_cost_diff: float
    avg_dmg: float
    avg_dmg_diff: float
    avg_hp: float
    avg_hp_diff: float
    avg_mspd: float
    avg_mspd_diff: float
    category_class: str
    description: str
    description_id: str
    dmg_base: int | None = None
    dmg_expected: float | None = None
    dmg_max: int | None = None
    dps: float | None = None
    flags: str
    gold_bounty: int | None = None
    gold_cost: int | None = None
    gold_value: int | None = None
    hp: int
    icon_path: str
    income_bonus: int | None = None
    info_sketchfab: str | None = None
    info_tier: str | None = None
    is_enabled: bool
    legion_id: str
    model_scale: float
    move_speed: int | None = None
    move_type: str | None = None
    mp: int | None = None
    mspd_text: str
    mythium_cost: int | None = None
    name: str
    radius: str
    range_text: str
    sort_order: str
    splash_path: str
    stock_max: int | None = None
    stock_time: int | None = None
    tooltip: str
    total_value: int | None = None
    unit_class: str
    upgrades_from: list[str] = Field(alias="upgradesFrom", sa_column=Column(JSON))

    class Config:
        arbitrary_types_allowed = True


class Unit(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True, alias="unit_id")
    name: str
    sort_order: str
    # def
    hp: int
    armor_type: ArmorTypes | None = None
    mp: int | None = None
    move_speed: int | None = None
    move_type: str | None = None
    # dmg
    attack_range: int | None = None
    attack_speed: float | None = None
    attack_type: AttackTypes | None = None
    dmg_base: int | None = None
    dps: float | None = None
    # info
    gold_cost: int | None = None
    total_value: int | None = None
    flags: str
    info_tier: str | None = None
    is_enabled: bool
    legion_id: str
    unit_class: str
    icon_path: str
    splash_path: str
    version: str
    upgrades_from: list[str] = Field(sa_column=Column(JSON))
    arena_id: int | None = Field(default=None, foreign_key="arena.id")
    arena: Optional["Arena"] = Relationship(back_populates="units")

    @computed_field
    def hp_vs_impact(self) -> float:
        if [x for x in (self.hp, self.armor_type) if x is None]:
            return 0
        return self.hp / damage_def_map.get(AttackTypes.IMPACT).get(self.armor_type)

    @computed_field
    def hp_vs_pierce(self) -> float:
        if [x for x in (self.hp, self.armor_type) if x is None]:
            return 0
        return self.hp / damage_def_map.get(AttackTypes.PIERCE).get(self.armor_type)

    @computed_field
    def hp_vs_magic(self) -> float:
        if [x for x in (self.hp, self.armor_type) if x is None]:
            return 0
        return self.hp / damage_def_map.get(AttackTypes.MAGIC).get(self.armor_type)

    @computed_field
    def hp_vs_pure(self) -> float:
        if [x for x in (self.hp, self.armor_type) if x is None]:
            return 0
        return self.hp / damage_def_map.get(AttackTypes.PURE).get(self.armor_type)

    @computed_field
    def dps_vs_swift(self) -> float:
        if [x for x in (self.dps, self.attack_type) if x is None]:
            return 0
        return self.dps * damage_def_map.get(self.attack_type).get(ArmorTypes.SWIFT)

    @computed_field
    def dps_vs_natural(self) -> float:
        if [x for x in (self.dps, self.attack_type) if x is None]:
            return 0
        return self.dps * damage_def_map.get(self.attack_type).get(ArmorTypes.NATURAL)

    @computed_field
    def dps_vs_fortified(self) -> float:
        if [x for x in (self.dps, self.attack_type) if x is None]:
            return 0
        return self.dps * damage_def_map.get(self.attack_type).get(ArmorTypes.FORTIFIED)

    @computed_field
    def dps_vs_arcane(self) -> float:
        if [x for x in (self.dps, self.attack_type) if x is None]:
            return 0
        return self.dps * damage_def_map.get(self.attack_type).get(ArmorTypes.ARCANE)

    @computed_field
    def dps_vs_immaterial(self) -> float:
        if [x for x in (self.dps, self.attack_type) if x is None]:
            return 0
        return self.dps * damage_def_map.get(self.attack_type).get(
            ArmorTypes.IMMATERIAL
        )


class StageCounter(SQLModel):
    id: str
    hp_vs_stage: float
    dps_vs_stage: float
    gold_cost: int

    @computed_field
    def hp_vs_stage_per_gold(self) -> float:
        return self.hp_vs_stage / self.gold_cost

    @computed_field
    def dps_vs_stage_per_gold(self) -> float:
        return self.dps_vs_stage / self.gold_cost

    @computed_field
    def dps_hp_value(self) -> float:
        return self.hp_vs_stage_per_gold * self.dps_vs_stage_per_gold


class ElementBaseUnits(SQLModel):
    proton: Unit
    aqua_spirit: Unit
    windhawk: Unit
    mudman: Unit
    disciple: Unit
    fire_lord: Unit


class Arena(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, ge=1, le=4)
    units: list[Unit] = Relationship(back_populates="arena")
    units_counter: dict[str, int] = Field(default={}, sa_column=Column(JSON))


class CreateUpdateArena(SQLModel):
    id: int = Field(ge=1, le=4)
    unit_ids: list[str]


class Stats(SQLModel):
    hp: list[int] = []
    dps: list[float] = []
    dmg_base: list[int] = []
    hp_vs_impact: list[float] = []
    hp_vs_pierce: list[float] = []
    hp_vs_magic: list[float] = []
    hp_vs_pure: list[float] = []
    dps_vs_swift: list[float] = []
    dps_vs_natural: list[float] = []
    dps_vs_fortified: list[float] = []
    dps_vs_arcane: list[float] = []
    dps_vs_immaterial: list[float] = []


class SummedStats(SQLModel):
    hp: int
    dps: float
    dmg_base: int
    hp_vs_impact: float
    hp_vs_pierce: float
    hp_vs_magic: float
    hp_vs_pure: float
    dps_vs_swift: float
    dps_vs_natural: float
    dps_vs_fortified: float
    dps_vs_arcane: float
    dps_vs_immaterial: float


class CreatureSummedStats(SummedStats):
    attack_type: AttackTypes
    armor_type: ArmorTypes


class ArenaStatsVsStage(SQLModel):
    # arena seconds to kill formula self.stage_hp / self.arena_vs_stage_dps_diff as damage modifier is applied
    # on the dps and it can be compared then with raw hp

    # diff can be compared raw to multiplier as multiplied stats are used in this model
    arena_hp_vs_stage_attack_type: float
    arena_dps_vs_stage_armor_type: float
    stage_attack_type: AttackTypes
    stage_armor_type: ArmorTypes
    stage_hp: float
    stage_dps: float

    @computed_field
    def arena_seconds_to_kill_stage(self) -> float:
        return self.stage_hp / self.arena_dps_vs_stage_armor_type

    @computed_field
    def stage_seconds_to_kill_arena(self) -> float:
        return self.arena_hp_vs_stage_attack_type / self.stage_dps

    @computed_field
    def arena_vs_stage_seconds_to_kill_diff(self) -> float:
        return self.arena_seconds_to_kill_stage - self.stage_seconds_to_kill_arena

    @computed_field
    def arena_vs_stage_hp_diff(self) -> float:
        return self.arena_hp_vs_stage_attack_type - self.stage_hp

    @computed_field
    def arena_vs_stage_dps_diff(self) -> float:
        return self.arena_dps_vs_stage_armor_type - self.stage_dps
