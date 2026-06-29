"""
Database session management
"""

import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from bot.config import Config
from db.models import Base

logger = logging.getLogger(__name__)

engine = create_async_engine(Config.DATABASE_URL, echo=Config.DEBUG, future=True)

async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    """Get database session"""
    return async_session_maker()


async def init_db():
    """Initialize database"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✅ Database initialized")


async def close_db():
    """Close database connection"""
    await engine.dispose()
    logger.info("✅ Database closed")
