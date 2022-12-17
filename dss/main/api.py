from fastapi import APIRouter
from dss.dss import dss_router
from dss.database import create_db_and_tables
router = APIRouter(prefix="/api")

@router.on_event("startup")
def on_startup():
    create_db_and_tables()

router.include_router(dss_router)
