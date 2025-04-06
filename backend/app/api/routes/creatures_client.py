import httpx

from app.models import CreatureSummedStats, StageCounter, Unit
from app.api.routes.units_client import read_element_units

prefix = "/creatures"
client = httpx.Client(base_url=f"http://localhost:8000/api/v1{prefix}")


def read_creatures() -> list[Unit]:
    response_json = client.get(url="").json()
    return [Unit(**unit) for unit in response_json]


def read_creatures_by_stage(stage: int) -> list[Unit]:
    response_json = client.get(url=f"/{stage}").json()
    return [Unit(**unit) for unit in response_json]


def calculate_stage_stats(stage: int) -> CreatureSummedStats:
    response_json = client.get(url=f"/{stage}/stats").json()
    return CreatureSummedStats(**response_json)


def sort_units_as_counters_by_stage(stage: int) -> list[StageCounter]:
    units=read_element_units()
    units_json = [unit.model_dump() for unit in units]
    response_json = client.post(url=f"/{stage}/counters", json=units_json).json()
    return [StageCounter(**unit) for unit in response_json]



