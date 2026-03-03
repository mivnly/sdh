from fastapi import APIRouter, FastAPI

from app.routers.common import common_router
from app.routers.users import users_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(common_router)
api_router.include_router(users_router)

app = FastAPI()
app.include_router(api_router)
