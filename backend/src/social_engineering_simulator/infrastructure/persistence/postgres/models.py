from datetime import datetime
from sqlalchemy import UUID, String, Enum as SAEnum, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from social_engineering_simulator.domain.organizations.department.employee.value_object import Email
from social_engineering_simulator.domain.organizations.value_object import IndustryType


class Base(DeclarativeBase):
    pass


class OrganizationModel(Base):
    __tablename__ = "organizations"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    industry: Mapped[IndustryType] = mapped_column(SAEnum(IndustryType, name="industry_type"))
    created_at: Mapped[datetime] = mapped_column()

    def __repr__(self) -> str:
        return f"Organization(id={self.id!r}, name={self.name!r}, idustry={self.industry!r})"


class DepartmentModel(Base):
    __tablename__ = "departments"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column()


class EmployeeModel(Base):
    __tablename__ = "employees"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[Email] = mapped_column()
    created_at: Mapped[datetime] = mapped_column()
    department_id: Mapped = mapped_column(ForeignKey("departments.id"))

