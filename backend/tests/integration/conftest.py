import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine

from social_engineering_simulator.infrastructure.persistence.postgres.models import Base

TEST_DATABASE_URL = f'postgresql+asyncpg://postgres:postgres@localhost:5433/simulator_test'


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
