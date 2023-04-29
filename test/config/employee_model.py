from sqlalchemy import Column, String, Boolean, Integer, DateTime, Float

from .base import Base


class Employee(Base):
    __tablename__ = "employee"
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )
    email = Column(
        String,
        index=True,
        nullable=False,
        unique=True,
        info={"alias_xlsx": "Email"},
    )
    entry_date = Column(
        DateTime,
        info={"alias_xlsx": "Entry date"},
    )
    salary = Column(
        Float,
        info={"alias_xlsx": "Salary"},
    )
    is_directive = Column(
        Boolean(),
        default=False,
        nullable=False,
        info={"alias_xlsx": "Is Directive?"},
    )

    def __repr__(self):
        return self.email
