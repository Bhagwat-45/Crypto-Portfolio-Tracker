from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from src.config.settings import settings
import logging

logger = logging.getLogger(__name__)

Base = declarative_base() 


sql_url = settings.database_url 

try:
    engine = create_async_engine(sql_url, echo=False, pool_size=50) 

    AsyncSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
except Exception as e:
    logger.error(f"Error creating Async Engine: {e}")
    engine = None
    AsyncSessionLocal = None


async def get_db_session():
    if AsyncSessionLocal is None:
        logger.error("AsyncSessionLocal is not initialized. Check DB URL.")
        return

    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()