# lib
from datetime import datetime
import pandas as pd

# orm
from sqlalchemy import and_

# session
from config.session import db_session

# model
from config.employee_model import Employee

# own lib
from alchemymodel_xlsx import import_data

import unittest


class TextImportFromExcel(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # set filename
        self.filename1 = "test1_employees.xlsx"
        self.filename2 = "test2_employees.xlsx"

        # set session
        self.db_session = db_session

        # set model
        self.model = Employee

        # get fiels from model
        self.fields = {
            c.key: c.info.get("alias_xlsx")
            for c in self.model.__table__.c
            if c.info.get("alias_xlsx")
        }

        # expresion boolean convert to str in excel
        self.expr_bool = {True: "Yes", False: "No"}

    def excel_type_data_to_pythontype(self, value: bool):
        if value in list(self.expr_bool.values()):
            return True if value == self.expr_bool[True] else False

        return str(value)

    def test_count_data_equal(self):
        file = open(self.filename, "rb")

        import_data(
            file=file,
            model=self.model,
            fields=self.fields,
            db_session=self.db_session,
            expr_bool=self.expr_bool,
        )

        # read excel data
        excel_file = pd.read_excel(self.filename, na_filter=None)

        # Get the number of rows in the DataFrame
        excel_row_count = len(excel_file)

        # labels keys to column keys
        data_from_excel = []

        for _, row in excel_file.iterrows():
            row_dict = row.to_dict()
            data = {}
            for key, value in row_dict.items():
                model_column = list(self.fields.keys())[
                    list(self.fields.values()).index(key)
                ]

                data[model_column] = self.excel_type_data_to_pythontype(value)

            data_from_excel.append(data)

        data_from_db = []

        for data in data_from_excel:
            fields_to_compare = [
                getattr(self.model, key) == value for key, value in data.items()
            ]
            row_in_db = (
                db_session.query(self.model).filter(and_(*fields_to_compare)).first()
            )

            if row_in_db:
                data_from_db.append(row_in_db)

        assert len(data_from_db) == excel_row_count

    def test_data_equal(self):
        file = open(self.filename, "rb")

        import_data(
            file=file,
            model=self.model,
            fields=self.fields,
            db_session=self.db_session,
            expr_bool=self.expr_bool,
        )

        # read excel data
        excel_file = pd.read_excel(self.filename, na_filter=None)

        # labels keys to column keys
        data_from_excel = []

        for _, row in excel_file.iterrows():
            row_dict = row.to_dict()
            data = {}
            for key, value in row_dict.items():
                model_column = list(self.fields.keys())[
                    list(self.fields.values()).index(key)
                ]

                data[model_column] = self.excel_type_data_to_pythontype(value)

            data_from_excel.append(data)

        data_from_db = []

        for data in data_from_excel:
            fields_to_compare = [
                getattr(self.model, key) == value for key, value in data.items()
            ]
            row_in_db = (
                db_session.query(self.model).filter(and_(*fields_to_compare)).first()
            )

            if row_in_db:
                row_to_dict = {}

                for c in self.model.__table__.c:
                    if c.key != "id":
                        value_from_row_db = getattr(row_in_db, c.key)

                        if isinstance(value_from_row_db, float):
                            value_from_row_db = str(int(value_from_row_db))

                        if isinstance(value_from_row_db, datetime):
                            value_from_row_db = str(value_from_row_db)

                        row_to_dict[c.key] = value_from_row_db

                data_from_db.append(row_to_dict)

        assert data_from_excel == data_from_db


def big_suite():
    test_classes_to_run = [TextImportFromExcel]
    loader = unittest.TestLoader()
    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)
    big_suite = unittest.TestSuite(suites_list)
    return big_suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(big_suite())
