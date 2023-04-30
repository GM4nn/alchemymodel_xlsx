# tests
from test_import_from_excel import TextImportFromExcel
from test_model_to_excel import TestModelToExcel
from test_model_to_csv import TestModelToCsv
from test_template import TestTemplate

# unitest
import unittest


def big_suite():
    test_classes_to_run = [
        TextImportFromExcel,
        TestModelToCsv,
        TestModelToExcel,
        TestTemplate,
    ]
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
