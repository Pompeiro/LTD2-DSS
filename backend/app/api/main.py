from fastapi import APIRouter

from app.api.routes import (
    arenas,
    creatures,
    images,
    items,
    login,
    ltd2_units,
    private,
    stats,
    units,
    users,
    utils,
)
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(items.router)
api_router.include_router(ltd2_units.router)
api_router.include_router(units.router)
arenas.router.include_router(stats.router)
api_router.include_router(arenas.router)
api_router.include_router(images.router)
api_router.include_router(creatures.router)

if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
