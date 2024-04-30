from fastapi import APIRouter

from app.api.routes import arenas, ltd2_units, stats, units

api_router = APIRouter()
# api_router.include_router(login.router, tags=["login"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(ltd2_units.router, prefix="/ltd2-units", tags=["ltd2-units"])
api_router.include_router(units.router, prefix="/units", tags=["units"])
arenas.router.include_router(stats.router, prefix="/{arena_id}/stats", tags=["stats"])
api_router.include_router(arenas.router, prefix="/arenas", tags=["arenas"])
