import os
from functools import wraps

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

sqlalchemy_database_uri = f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"  # noqa: E501
engine = create_async_engine(sqlalchemy_database_uri, future=True, echo=True)
session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with session_factory() as session:
        yield session
    await session.close()


def set_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with session_factory() as session:
            kwargs["session"] = session
            return await func(*args, **kwargs)

    return wrapper
