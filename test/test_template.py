# lib
from os.path import dirname
from os.path import abspath
from os.path import join
from io import BytesIO
import pandas as pd
import sys

from sqlalchemy import Boolean

# session
from config.session import db_session

# model
from config.employee_model import Employee

# add dir
sys.path.insert(0, abspath(join(dirname(__file__), "..")))

# own lib
from alchemymodel_xlsx import create_template

import unittest


class TestTemplate(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # set model
        self.model = Employee

        # get fiels from model
        self.fields = {
            c.key: c.info.get("alias_xlsx")
            for c in self.model.__table__.c
            if c.info.get("alias_xlsx")
        }

    def test_create_template(self):
        xlsx_file = create_template(
            model=self.model,
            fields=self.fields,
        )

        assert bytes == type(xlsx_file)

    def test_equal_columns(self):
        xlsx_file = create_template(
            model=self.model,
            fields=self.fields,
        )

        excel_file = pd.read_excel(BytesIO(xlsx_file), na_filter=None)
        column_names = list(excel_file.columns)
        model_fields = list(self.fields.values())
        column_names.sort()
        model_fields.sort()

        assert column_names == model_fields


def big_suite():
    test_classes_to_run = [TestTemplate]
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
