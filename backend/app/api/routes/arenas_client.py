import httpx

from app.models import Arena, ArenaStatsVsStage

prefix = "/arenas"
client = httpx.Client(base_url=f"http://localhost:8000/api/v1{prefix}")


def read_arena(arena_id: int = 1) -> Arena:
    response_json = client.get(url=f"/{arena_id}").json()
    return Arena(**response_json)


def update_arena(
    units: list[str], arena_id: int = 1, clear_units: bool = True
) -> Arena:
    params = {"clear_units": clear_units}
    response_json = client.put(url=f"/{arena_id}", params=params, json=units).json()
    return Arena(**response_json)


def compare_arena_vs_stage_stats(
    arena_id: int = 1, stage_id: int = 1
) -> ArenaStatsVsStage:
    response_json = client.get(url=f"/{arena_id}/stats/{stage_id}/compare").json()
    return ArenaStatsVsStage(**response_json)
