from typing import Optional

from sqlmodel import Field, SQLModel


class Unit(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    name: str
    # def
    hp: int
    armor_type: str
    mp: Optional[int] = Field(default=None)
    move_speed: Optional[int] = Field(default=None)
    move_type: str
    # dmg
    attack_range: Optional[int] = Field(default=None)
    attack_speed: Optional[float] = Field(default=None)
    attack_type: str
    dmg_base: Optional[int] = Field(default=None)
    dps: Optional[float] = Field(default=None)
    # info
    gold_cost: Optional[int] = Field(default=None)
    total_value: Optional[int] = Field(default=None)
    flags: str
    info_tier: str
    is_enabled: bool
    legion_id: str
    unit_class: str
    icon_path: str
    splash_path: str
    version: str
