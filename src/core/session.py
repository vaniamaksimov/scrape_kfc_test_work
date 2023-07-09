from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from src.core.settings import settings

engine = create_async_engine(url=settings.db.url)
session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)
AsyncSessionLocal = async_scoped_session(session_factory, scopefunc=current_task)
