from sqlmodel import JSON, Column, Field, Relationship, SQLModel

from ..units.models import UnitArenaLink


class Arena(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    units: list["Unit"] = Relationship(  # type: ignore[name-defined]
        back_populates="arenas", link_model=UnitArenaLink
    )
    units_counter: dict[str, int] = Field(default={}, sa_column=Column(JSON))


class CreateUpdateArena(SQLModel):
    id: int
    unit_ids: list[str]
