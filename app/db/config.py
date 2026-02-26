from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings


_engine = create_async_engine(
    settings.conn_url.encoded_string(),
    echo=False,
    pool_pre_ping=True
)

asession_maker = async_sessionmaker(
    bind=_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with asession_maker() as asession:
        yield asession
