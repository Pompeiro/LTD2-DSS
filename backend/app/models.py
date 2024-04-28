from pydantic import field_validator
from sqlmodel import JSON, Column, Field, Relationship, SQLModel


# Shared properties
# TODO replace email str with EmailStr when sqlmodel supports it
class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str


# TODO replace email str with EmailStr when sqlmodel supports it
class UserRegister(SQLModel):
    email: str
    password: str
    full_name: str | None = None


# Properties to receive via API on update, all are optional
# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdate(UserBase):
    email: str | None = None  # type: ignore
    password: str | None = None


# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdateMe(SQLModel):
    full_name: str | None = None
    email: str | None = None


class UpdatePassword(SQLModel):
    current_password: str
    new_password: str


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner")


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: int


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str
    description: str | None = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = None  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: int
    owner_id: int


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
    sub: int | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str


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
