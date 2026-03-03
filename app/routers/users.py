from typing import Annotated

from asyncpg.exceptions import UniqueViolationError
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import users
from app.db.config import get_session
from app.db.models import User
from app.schemas.users import UserCreate, UserRead, UserUpdate

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.get("/", response_model=list[UserRead])
async def get_users(
    session: Annotated[AsyncSession, Depends(get_session)],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
) -> list[User]:
    return await users.read(session, limit=limit)


@users_router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(
    user_id: int,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> User:
    user = await users.read(session, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User with provided ID is not found")
    return user


@users_router.post("/", response_model=UserCreate, status_code=status.HTTP_201_CREATED)
async def add_user(
    session: Annotated[AsyncSession, Depends(get_session)],
    new_user: UserCreate,
) -> User:
    try:
        return await users.create(session, obj_in=new_user)
    except UniqueViolationError as e:
        raise HTTPException(
            409, f"The username '{new_user.username}' is already taken. Please try a different one."
        ) from e


@users_router.put("/{user_id}", response_model=UserUpdate)
async def update_user(
    session: Annotated[AsyncSession, Depends(get_session)], user_id: int, user_to_update: UserUpdate
) -> User:
    db_user = await users.read(session, user_id=user_id)
    if db_user is None:
        raise HTTPException(404, "User with provided ID is not found")

    try:
        return await users.update(session=session, db_obj=db_user, obj_in=user_to_update)
    except UniqueViolationError as e:
        raise HTTPException(
            409, f"The username '{user_to_update.username}' is already taken. Please try a different one."
        ) from e


@users_router.delete("/{user_id}", response_model=UserRead)
async def delete_user(session: Annotated[AsyncSession, Depends(get_session)], user_id: int):
    db_user = await users.read(session, user_id=user_id)
    if db_user is None:
        raise HTTPException(404, "User with provided ID is not found")

    return await users.delete(session=session, db_obj=db_user)
