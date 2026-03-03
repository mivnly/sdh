from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import log
from app.db.config import _engine, asession_maker
from app.db.models import Base


async def get_tables(session: AsyncSession, schema: str = "public") -> list[str]:
    stmt = text(
        "SELECT table_name FROM information_schema.tables WHERE table_schema = :schema AND table_type = 'BASE TABLE'"
    )
    result = await session.execute(stmt, {"schema": schema})
    return [row[0] for row in result.all()]


async def create_all_tables() -> None:
    async with asession_maker() as session:
        before = await get_tables(session)

    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all, checkfirst=True)

    async with asession_maker() as session:
        after = await get_tables(session)

    difference = [table for table in after if table not in before]
    as_str = ", ".join(difference)
    message = f"Created tables: {as_str}" if difference else "All tables have already been created"
    log.info(message)
