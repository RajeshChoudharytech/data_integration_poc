from fastapi import APIRouter

from .routes.destination import router as destination_router
from .routes.source import router as source_router
from .routes.sync import router as sync_router
from .routes.user import router as user_router

api_router = APIRouter()

api_router.include_router(
    source_router, prefix="/source", tags=["source"]
)
api_router.include_router(destination_router, prefix="/destination", 
                          tags=["destination"])
api_router.include_router(sync_router, prefix="/sync", tags=["sync"])
api_router.include_router(user_router, prefix="/user", tags=["user"])
