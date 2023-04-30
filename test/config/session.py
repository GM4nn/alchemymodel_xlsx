# sqlalchemy
from sqlalchemy_utils import create_database
from sqlalchemy_utils import database_exists
from sqlalchemy_utils import drop_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# app
from .employee_model import Employee
from .base import Base

# consts
from .const import SQLALCHEMY_DATABASE_URI


engine = create_engine(SQLALCHEMY_DATABASE_URI)
if database_exists(engine.url):
    drop_database(engine.url)

create_database(engine.url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = SessionLocal()

# Create all tables that do not already exist
Base.metadata.create_all(engine)


# insert data to employee
employee1 = Employee(
    email="gr_sql_model_v1@example.com",
    entry_date="2022-01-01",
    salary=None,
    is_directive=True,
)
employee2 = Employee(
    email="gr_sql_model_v2@example.com",
    entry_date="2020-01-01",
    salary=1500,
    is_directive=False,
)

db_session.bulk_save_objects([employee1, employee2])
db_session.commit()
