from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.config import get_session
from app.schemas.users import UserRead
from app.crud import users


router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserRead])
async def get_users(
    session: Annotated[AsyncSession, Depends(get_session)],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    username: Annotated[str | None, Query(min_length=2, max_length=80)] = None
):
    if username is not None:
        user = await users.read(session, username=username)
        return [user] if user else []
    return await users.read(session, limit=limit)

@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(
    user_id: int,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    user = await users.read(session, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User with provided ID is not found")
    return user
