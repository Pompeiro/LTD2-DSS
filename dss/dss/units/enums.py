from enum import StrEnum


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
