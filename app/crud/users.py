from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User

async def get(db: AsyncSession, limit: int = 100) -> list[User]:
    result = await db.execute(select(User).limit(limit))
    return list(result.scalars().all())
