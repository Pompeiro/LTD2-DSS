from fastapi import APIRouter

from dss.database import create_db_and_tables
from dss.dss import dss_router

router = APIRouter(prefix="/api")


@router.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()


router.include_router(dss_router)
