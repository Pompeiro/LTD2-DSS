from sqlmodel import SQLModel


class Stats(SQLModel):
    hp: list = []
    dps: list = []
    dmg_base: list = []
    hp_vs_impact: list = []
    hp_vs_pierce: list = []
    hp_vs_magic: list = []
    hp_vs_pure: list = []
    dmg_vs_swift: list = []
    dmg_vs_natural: list = []
    dmg_vs_fortified: list = []
    dmg_vs_arcane: list = []
    dmg_vs_immaterial: list = []
