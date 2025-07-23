from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy import text
import asyncio

from app.core.config import settings
from app.db.base import Base

# Create engine for async PostgreSQL connection
engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)

# Dependency for getting DB session
async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# Dependency for route injection
async def get_db():
    async with async_session() as session:
        yield session


# Initialize database (create tables)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
