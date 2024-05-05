from enum import IntEnum, StrEnum


class AttackTypes(StrEnum):
    IMPACT = ("Impact",)
    PIERCE = ("Pierce",)
    MAGIC = ("Magic",)
    PURE = "Pure"


class ArmorTypes(StrEnum):
    SWIFT = ("Swift",)
    NATURAL = ("Natural",)
    FORTIFIED = ("Fortified",)
    ARCANE = ("Arcane",)
    IMMATERIAL = "Immaterial"


class ArenaGrid(IntEnum):
    X1 = (550,)
    X2 = (775,)
    Y1 = (380,)
    Y2 = (715,)
    MARGIN = 10


IMPACT_VS_SWIFT = 0.8
IMPACT_VS_NATURAL = 0.9
IMPACT_VS_FORTIFIED = 1.15
IMPACT_VS_ARCANE = 1.15
IMPACT_VS_IMMATERIAL = 1.0

PIERCE_VS_SWIFT = 1.20
PIERCE_VS_NATURAL = 0.85
PIERCE_VS_FORTIFIED = 0.8
PIERCE_VS_ARCANE = 1.15
PIERCE_VS_IMMATERIAL = 1.0

MAGIC_VS_SWIFT = 1.0
MAGIC_VS_NATURAL = 1.25
MAGIC_VS_FORTIFIED = 1.05
MAGIC_VS_ARCANE = 0.75
MAGIC_VS_IMMATERIAL = 1.0

PURE_VS_SWIFT = 1.0
PURE_VS_NATURAL = 1.0
PURE_VS_FORTIFIED = 1.0
PURE_VS_ARCANE = 1.0
PURE_VS_IMMATERIAL = 1.0

damage_def_map = {
    AttackTypes.IMPACT: {
        ArmorTypes.SWIFT: IMPACT_VS_SWIFT,
        ArmorTypes.NATURAL: IMPACT_VS_NATURAL,
        ArmorTypes.FORTIFIED: IMPACT_VS_FORTIFIED,
        ArmorTypes.ARCANE: IMPACT_VS_ARCANE,
        ArmorTypes.IMMATERIAL: IMPACT_VS_IMMATERIAL,
    },
    AttackTypes.PIERCE: {
        ArmorTypes.SWIFT: PIERCE_VS_SWIFT,
        ArmorTypes.NATURAL: PIERCE_VS_NATURAL,
        ArmorTypes.FORTIFIED: PIERCE_VS_FORTIFIED,
        ArmorTypes.ARCANE: PIERCE_VS_ARCANE,
        ArmorTypes.IMMATERIAL: PIERCE_VS_IMMATERIAL,
    },
    AttackTypes.MAGIC: {
        ArmorTypes.SWIFT: MAGIC_VS_SWIFT,
        ArmorTypes.NATURAL: MAGIC_VS_NATURAL,
        ArmorTypes.FORTIFIED: MAGIC_VS_FORTIFIED,
        ArmorTypes.ARCANE: MAGIC_VS_ARCANE,
        ArmorTypes.IMMATERIAL: MAGIC_VS_IMMATERIAL,
    },
    AttackTypes.PURE: {
        ArmorTypes.SWIFT: PURE_VS_SWIFT,
        ArmorTypes.NATURAL: PURE_VS_NATURAL,
        ArmorTypes.FORTIFIED: PURE_VS_FORTIFIED,
        ArmorTypes.ARCANE: PURE_VS_ARCANE,
        ArmorTypes.IMMATERIAL: PURE_VS_IMMATERIAL,
    },
}

creatures_amount_map = {
    "Crab": 12,
    "Wale": 12,
    "Hopper": 18,
    "Flying Chicken": 12,
    "Scorpion": 8,
    "Scorpion King": 1,
    "Rocko": 6,
    "Sludge": 10,
    "Kobra": 12,
    "Carapace": 12,
    "Granddaddy": 1,
    "Quil Shooter": 12,
    "Mantis": 12,
    "Drill Golem": 6,
    "Killer Slug": 12,
    "Quadrapus": 8,
    "Giant Quadrapus": 1,
    "Cardinal": 18,
    "Metal Dragon": 12,
    "Wale Chief": 6,
    "Dire Toad": 12,
    "Maccabeus": 1,
    "Legion Lord": 10,
    "Legion King": 1,
}

stage_attack_to_arena_hp_vs_map: dict[AttackTypes, str] = {
    AttackTypes.IMPACT: "hp_vs_impact",
    AttackTypes.PIERCE: "hp_vs_pierce",
    AttackTypes.MAGIC: "hp_vs_magic",
    AttackTypes.PURE: "hp_vs_pure",
}

stage_armor_to_arena_dps_vs_map: dict[ArmorTypes, str] = {
    ArmorTypes.SWIFT: "dps_vs_swift",
    ArmorTypes.NATURAL: "dps_vs_natural",
    ArmorTypes.FORTIFIED: "dps_vs_fortified",
    ArmorTypes.ARCANE: "dps_vs_arcane",
    ArmorTypes.IMMATERIAL: "dps_vs_immaterial",
}
