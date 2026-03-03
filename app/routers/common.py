from fastapi import APIRouter

common_router = APIRouter(prefix="/health", tags=["health"])


@common_router.get("/")
async def health_check():
    return {"status": "ok"}
