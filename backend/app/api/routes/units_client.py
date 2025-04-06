import httpx

from app.models import Unit

prefix = "/units"
client = httpx.Client(base_url=f"http://localhost:8000/api/v1{prefix}")


def read_element_units() -> list[Unit]:
    response_json = client.get(url="/element").json()
    return [Unit(**unit) for unit in response_json]
