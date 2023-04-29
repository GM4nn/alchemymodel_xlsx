# lib
from os.path import dirname
from os.path import abspath
from os.path import join
from io import BytesIO
import pandas as pd

from sqlalchemy import Boolean

# own lib
from alchemymodel_xlsx import query_to_excel

# session
from config.session import db_session

# model
from config.employee_model import Employee


import unittest


class TestModelToExcel(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # set model
        self.model = Employee

        # set query
        self.query = db_session.query(self.model).order_by(self.model.id.desc())

        # get fiels from model
        self.fields = {
            c.key: c.info.get("alias_xlsx")
            for c in self.model.__table__.c
            if c.info.get("alias_xlsx")
        }

        # expresion boolean convert to str in excel
        self.expr_bool = {True: "Yes", False: "No"}

    def test_data_to_excel_in_bytes(self):
        xlsx_file = query_to_excel(
            query=self.query,
            fields=self.fields,
            expr_bool=self.expr_bool,
        )

        assert bytes == type(xlsx_file)

    def test_equal_columns(self):
        xlsx_file = query_to_excel(
            query=self.query,
            fields=self.fields,
            expr_bool=self.expr_bool,
        )

        excel_file = pd.read_excel(BytesIO(xlsx_file), na_filter=None)
        column_names = list(excel_file.columns)
        model_fields = list(self.fields.values())
        column_names.sort()
        model_fields.sort()

        assert column_names == model_fields

    def test_equal_expr_bool(self):
        xlsx_file = query_to_excel(
            query=self.query,
            fields=self.fields,
            expr_bool=self.expr_bool,
        )
        excel_file = pd.read_excel(BytesIO(xlsx_file), na_filter=None)

        boolean_columns = [
            c.info.get("alias_xlsx")
            for c in self.model.__table__.c
            if isinstance(c.type, Boolean) and c.info.get("alias_xlsx")
        ]

        for _, row in excel_file.iterrows():
            row_dict = row.to_dict()

            for boolean_column in boolean_columns:
                assert row_dict[boolean_column] in list(self.expr_bool.values())


def big_suite():
    test_classes_to_run = [TestModelToExcel]
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