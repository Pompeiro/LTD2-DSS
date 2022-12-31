from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from .enums import ArmorTypes, AttackTypes, damage_def_map


class UnitArenaLink(SQLModel, table=True):
    arena_id: Optional[int] = Field(
        default=None, foreign_key="arena.id", primary_key=True
    )
    unit_id: Optional[str] = Field(
        default=None, foreign_key="unit.id", primary_key=True
    )


class Unit(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True, alias="unit_id")
    name: str
    # def
    hp: int
    armor_type: Optional[ArmorTypes] = Field(default=None)
    mp: Optional[int] = Field(default=None)
    move_speed: Optional[int] = Field(default=None)
    move_type: str
    # dmg
    attack_range: Optional[int] = Field(default=None)
    attack_speed: Optional[float] = Field(default=None)
    attack_type: Optional[AttackTypes] = Field(default=None)
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
    arenas: list["Arena"] = Relationship(  # type: ignore[name-defined]
        back_populates="units", link_model=UnitArenaLink
    )

    @property
    def hp_vs_impact(self):  # type: ignore[no-untyped-def]
        return self.hp / damage_def_map.get(AttackTypes.IMPACT).get(self.armor_type)

    @property
    def hp_vs_pierce(self):  # type: ignore[no-untyped-def]
        return self.hp / damage_def_map.get(AttackTypes.PIERCE).get(self.armor_type)

    @property
    def hp_vs_magic(self):  # type: ignore[no-untyped-def]
        return self.hp / damage_def_map.get(AttackTypes.MAGIC).get(self.armor_type)

    @property
    def hp_vs_pure(self):  # type: ignore[no-untyped-def]
        return self.hp / damage_def_map.get(AttackTypes.PURE).get(self.armor_type)

    @property
    def dmg_vs_swift(self):  # type: ignore[no-untyped-def]
        return self.dmg_base * damage_def_map.get(self.attack_type).get(
            ArmorTypes.SWIFT
        )

    @property
    def dmg_vs_natural(self):  # type: ignore[no-untyped-def]
        return self.dmg_base * damage_def_map.get(self.attack_type).get(
            ArmorTypes.NATURAL
        )

    @property
    def dmg_vs_fortified(self):  # type: ignore[no-untyped-def]
        return self.dmg_base * damage_def_map.get(self.attack_type).get(
            ArmorTypes.FORTIFIED
        )

    @property
    def dmg_vs_arcane(self):  # type: ignore[no-untyped-def]
        return self.dmg_base * damage_def_map.get(self.attack_type).get(
            ArmorTypes.ARCANE
        )

    @property
    def dmg_vs_immaterial(self):  # type: ignore[no-untyped-def]
        return self.dmg_base * damage_def_map.get(self.attack_type).get(
            ArmorTypes.IMMATERIAL
        )
