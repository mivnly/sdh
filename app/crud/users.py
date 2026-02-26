from typing import overload
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import log
from app.db.models import User
from app.schemas.users import UserCreate, UserUpdate


async def create(session: AsyncSession, *, obj_in: UserCreate) -> User:
    db_obj = User(**obj_in.model_dump(exclude_unset=True))
    session.add(db_obj)
    try:
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    except IntegrityError as e:
        await session.rollback()
        msg = str(e.orig)
        log.error(msg)
    return db_obj

@overload
async def read(session: AsyncSession, limit: int | None = 100) -> list[User]:
    ...

@overload
async def read(session: AsyncSession, *, user_id: int) -> User | None:
    ...

@overload
async def read(session: AsyncSession, *, username: str) -> User | None:
    ...

async def read(session: AsyncSession, limit: int | None = 100, *, user_id: int | None = None, username: str | None = None) -> list[User] | User | None:
    if user_id:
        return await session.get(User, user_id)
    
    if username:
        result = await session.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    result = await session.execute(select(User).limit(limit))
    return list(result.scalars().all())

async def update(session: AsyncSession, *, db_obj: User, obj_in: UserUpdate) -> User:
    update_data = obj_in.model_dump(exclude_unset=True)
    if not update_data:
        raise ValueError("No fields provided for update")

    changes = {}
    for key, new_value in update_data.items():
        current_value = getattr(db_obj, key)
        
        if current_value != new_value:
            changes[key] = {"before": current_value, "after": new_value}
            setattr(db_obj, key, new_value)

    if not changes:
        log.warning("Given <obj_in> equals <db_obj>. There is nothing to update")
        return db_obj

    await session.commit()
    await session.refresh(db_obj)
    log.info(f"User {db_obj.username} has been changed: {changes}")
    return db_obj

async def delete(session: AsyncSession, *, db_obj: User) -> User:
    await session.delete(db_obj)
    await session.commit()
    log.info(f"User has been deleted: {db_obj}")
    return db_obj
