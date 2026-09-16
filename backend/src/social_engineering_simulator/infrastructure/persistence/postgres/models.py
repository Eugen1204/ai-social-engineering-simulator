from datetime import datetime
from uuid import UUID

from sqlalchemy import UUID as SAUUID, String, Enum as SAEnum, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class OrganizationModel(Base):
    __tablename__ = "organizations"

    id: Mapped[UUID] = mapped_column(SAUUID(as_uuid=True), primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    industry: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    departments: Mapped[list['DepartmentModel']] = relationship(back_populates="organization",
                                                                cascade="all, delete-orphan",
                                                                passive_deletes=True)

    def __repr__(self) -> str:
        return f"Organization(id={self.id!r}, name={self.name!r}, industry={self.industry!r})"


class DepartmentModel(Base):
    __tablename__ = "departments"

    id: Mapped[UUID] = mapped_column(SAUUID(as_uuid=True), primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    employees: Mapped[list["EmployeeModel"]] = relationship(back_populates="department", cascade="all, delete-orphan",
                                                            passive_deletes=True)
    organization_id: Mapped[UUID] = mapped_column(ForeignKey("organizations.id", ondelete='CASCADE'), nullable=False)
    organization: Mapped['OrganizationModel'] = relationship(back_populates='departments')

    def __repr__(self) -> str:
        return f"Department(id={self.id!r}, name={self.name!r})"


class EmployeeModel(Base):
    __tablename__ = "employees"

    id: Mapped[UUID] = mapped_column(SAUUID(as_uuid=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(254), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    department_id: Mapped[UUID] = mapped_column(ForeignKey("departments.id", ondelete='CASCADE'), nullable=False)

    department: Mapped["DepartmentModel"] = relationship(back_populates="employees")

    def __repr__(self) -> str:
        return f"Employee(id={self.id!r}, name={self.name!r}, email={self.email!r})"

