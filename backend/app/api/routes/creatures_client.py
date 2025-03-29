import httpx

from app.models import CreatureSummedStats, Unit

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
