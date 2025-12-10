from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool
import os


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite+aiosqlite:///./newshub.db"
)

if DATABASE_URL.startswith("sqlite"):
    engine = create_async_engine(
        DATABASE_URL,
        echo=True,
        connect_args={"check_same_thread": False},
        poolclass=NullPool
    )
else:
    engine = create_async_engine(
        DATABASE_URL,
        echo=True,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=3600
    )

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            print(f"Database error: {e}")
            raise
        finally:
            await session.close()