from decimal import Decimal
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncConnection
from sqlalchemy.orm import DeclarativeBase, registry, mapped_column
from sqlalchemy import String, MetaData, Numeric, INTEGER, DATETIME, Date
from typing_extensions import Annotated
import contextlib
from typing import Any, AsyncIterator
from datetime import datetime, date
from sqlalchemy import text, TEXT

from config import settings

metadata_obj = MetaData(schema=f"{settings.DB_SCHEMA}")

intpk = Annotated[int, mapped_column(primary_key=True)]
str_50 = Annotated[str, 50]
str_255 = Annotated[str, 255]
str_500 = Annotated[str, 500]
str_1000 = Annotated[str, 1000]
num_22_2 = Annotated[Decimal, 22]
num_18_6 = Annotated[Decimal, 18]
created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE( 'UTC' ,now())"))]
updated_at = Annotated[
    datetime, mapped_column(server_default=text("TIMEZONE( 'UTC' ,now())"), onupdate=text("TIMEZONE( 'UTC' ,now())"))]


class Base(DeclarativeBase):
    metadata = metadata_obj
    registry = registry(
        type_annotation_map={
            str_50: String(50),
            str_255: String(255),
            str_500: String(500),
            str_1000: String(1000),
            num_22_2: Numeric(22, 2),
            num_18_6: Numeric(18, 6),
            str: TEXT,
            date: Date,
        }
    )


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}):
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self) -> object:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(settings.database_url_asyncpg, {"echo": settings.ECHO_SQL})


async def get_db_session():
    async with sessionmanager.session() as session:
        yield session
