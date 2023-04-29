# lib
from os.path import dirname
from os.path import abspath
from os.path import join
from io import BytesIO
import sys

# session
from config.session import db_session

# model
from config.employee_model import Employee

# add dir
sys.path.insert(0, abspath(join(dirname(__file__), "..")))

# own lib
from alchemymodel_xlsx import model_to_excel
from alchemymodel_xlsx import model_to_csv
from alchemymodel_xlsx import create_template
from alchemymodel_xlsx import import_data


def users_to_excel():
    query_users = db_session.query(Employee).order_by(Employee.id.desc())

    xlsx_file = model_to_excel(
        model=Employee,
        query=query_users,
        expr_bool={True: "Si", False: "No"},
    )

    filename = "test.xlsx"
    f = open(filename, "wb")
    f.write(xlsx_file)
    f.close()


def user_to_csv():
    query_users = db_session.query(Employee).order_by(Employee.id.desc())

    xlsx_file = model_to_csv(
        model=Employee,
        query=query_users,
        fields={
            "email": "El email",
            "is_directive": "El active",
        },
        expr_bool={True: "Si", False: "No"},
    )

    filename = "test.xlsx"
    f = open(filename, "wb")
    f.write(xlsx_file)
    f.close()


def format_excel_users():
    xlsx_file = create_template(
        model=Employee,
    )

    filename = "format_employees.xlsx"
    f = open(filename, "wb")
    f.write(xlsx_file)
    f.close()


def create_users_from_excel():
    filename = "employees.xlsx"
    file = open(filename, "rb").read()

    import_data(
        BytesIO(file),
        Employee,
        fields={
            "email": "El email",
            "is_directive": "El active",
        },
        db_session=db_session,
        expr_bool={True: "Si", False: "No"},
    )


create_users_from_excel()
