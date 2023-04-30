
# Alchemy Model Xlsx

A library to management excel from SQLAlchemy queries.


Import data
---------
Create declarative base

.. code-block:: python
    
    from sqlalchemy.orm import declarative_base

    Base = declarative_base()

Create model

.. code-block:: python

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

Import data from excel to employee model

.. code-block:: python

    # other libs
    from io import BytesIO

    # alchemymodel_xlsx
    from alchemymodel_xlsx import import_data

    # model
    from .employee_model import Employee

    filename = "employees.xlsx"
    file = open(filename, "rb").read()

    import_data(
        BytesIO(file),
        Employee,
        fields={
            "email": "Email",
            "is_directive": "Is Directive?",
            "salary": "Salary"
        },
        db_session=db_session,
        expr_bool={True: "Si", False: "No"},
    )

Import data from excel to employee model with alias.
To define aliases on model attributes, you can od the following in specific attributes:

.. code-block:: python
    
    email = Column(
        String,
        index=True,
        nullable=False,
        unique=True,
        info={"alias_xlsx": "Email"},
    )

in this example we define with a parameter called "info" a dictionary where its key is "alias_xlsx" and its value will be the name we want to be shown in the excel column. Then:

.. code-block:: python
    
    fields = {
        c.key: c.info.get("alias_xlsx")
        for c in Employee.__table__.c
        if c.info.get("alias_xlsx")
    }

We get all the attributes where this alias exists, in this way we build a dictionary which waits for the library

.. code-block:: python 
    
    # other libs
    from io import BytesIO

    # alchemymodel_xlsx
    from alchemymodel_xlsx import import_data

    # model
    from .employee_model import Employee

    filename = "employees.xlsx"
    file = open(filename, "rb").read()

    fields = {
        c.key: c.info.get("alias_xlsx")
        for c in Employee.__table__.c
        if c.info.get("alias_xlsx")
    }

    import_data(
        BytesIO(file),
        Employee,
        fields=fields,
        db_session=db_session,
        expr_bool={True: "Si", False: "No"},
    )


## Create custom template

To create custom template, we can define custom aliases fields

.. code-block:: python
    
    from alchemymodel_xlsx import create_template
    
    xlsx_file = create_template(
        fields={
            "email": "Email",
            "is_directive": "Is Directive?",
            "salary": "Salary"
        },
    )

    filename = "format_employees.xlsx"
    f = open(filename, "wb")
    f.write(xlsx_file)
    f.close()

or get aliases fiels from our model

.. code-block:: python
    
    # model
    from .employee_model import Employee

    # alchemymodel_xlsx
    from alchemymodel_xlsx import create_template
    
    fields = {
        c.key: c.info.get("alias_xlsx")
        for c in Employee.__table__.c
        if c.info.get("alias_xlsx")
    }

    xlsx_file = create_template(
        fields=fields,
    )

    filename = "template_employees.xlsx"
    f = open(filename, "wb")
    f.write(xlsx_file)
    f.close()

    
## Export data to excel

to export data from a query, we can define a query where we can define filters and orders, so that when exporting, it takes the filters and orders and applies them.

.. code-block:: python

    # model
    from .employee_model import Employee

    # alchemymodel_xlsx
    from alchemymodel_xlsx import query_to_excel

    query_employees = db_session.query(Employee).order_by(Employee.id.desc())

    # get aliases fields from model
    fields = {
        c.key: c.info.get("alias_xlsx")
        for c in Employee.__table__.c
        if c.info.get("alias_xlsx")
    }

    xlsx_file = query_to_excel(
        query=query_employees,
        fields=fields,
        expr_bool={True: "Yes", False: "No"},
    )

    filename = "employees_export.xlsx"
    f = open(filename, "wb")
    f.write(xlsx_file)
    f.close()
## Export data to csv

Same procedure but now to export to csv

.. code-block:: python

    # model
    from .employee_model import Employee

    # alchemymodel_xlsx
    from alchemymodel_xlsx import query_to_csv

    query_employees = db_session.query(Employee).order_by(Employee.id.desc())

    # get aliases fields from model
    fields = {
        c.key: c.info.get("alias_xlsx")
        for c in Employee.__table__.c
        if c.info.get("alias_xlsx")
    }

    xlsx_file = query_to_csv(
        query=query_employees,
        fields=fields,
        expr_bool={True: "Yes", False: "No"},
    )

    filename = "employees_export.csv"
    f = open(filename, "wb")
    f.write(xlsx_file)
    f.close()
## Boolean expressions

To define boolean expressions both for exporting and importing data, we send as parameter "expr_bool" a dictionary where there will be two keys, True and False, and their values will be the ones that will be reflected when exporting, and when importing, it will take those values from the file and convert them to boolean values.

.. code-block:: python

    # model
    from .employee_model import Employee

    # alchemymodel_xlsx
    from alchemymodel_xlsx import query_to_excel

    # get aliases fields from model
    fields = {
        c.key: c.info.get("alias_xlsx")
        for c in Employee.__table__.c
        if c.info.get("alias_xlsx")
    }

    boolean_values = {True: "Yeah", False: "Oh no!"}

    xlsx_file = query_to_excel(
        query=query_employees,
        fields=fields,
        expr_bool=boolean_values,
    )