from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator

from config import DB_NAME, DB_PASS, DB_PORT, DB_USER  # type: ignore

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_PORT}/{DB_NAME}"

engine = create_async_engine(
    url=SQLALCHEMY_DATABASE_URL, echo=True
)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base: DeclarativeMeta = declarative_base()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
