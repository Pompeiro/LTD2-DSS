from fastapi import APIRouter

from app.api.routes import items, login, ltd2_units, users, utils

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(ltd2_units.router, prefix="/ltd2-units", tags=["ltd2-units"])
