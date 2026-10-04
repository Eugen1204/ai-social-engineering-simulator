from sqlalchemy.ext.asyncio import AsyncSession

from social_engineering_simulator.domain.organizations.unit_of_work import UnitOfWork
from social_engineering_simulator.infrastructure.persistence.postgres.organization_repository import \
    PostgresOrganizationRepository


class PostgresUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.organization = PostgresOrganizationRepository(session)

    async def __aenter__(self) -> "PostgresUnitOfWork":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
