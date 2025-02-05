from datetime import datetime

from config import TIMEZONE, ENGINE
from database.models import Base
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


engine = create_async_engine(url=ENGINE, echo=False)
async_session = async_sessionmaker(engine)


async def run_database():
    async with engine.begin() as conn:
        await conn.execute(text(f"SET TIME ZONE 'UTC{datetime.now(TIMEZONE).utcoffset().total_seconds() / 3600:+.0f}';"))
        await conn.run_sync(Base.metadata.create_all)

async def text_query(query: str):
    async with async_session() as session:
        await session.execute(text(query))
        await session.commit()


    