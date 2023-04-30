import os
from codecs import open
from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.rst"), "r", "utf-8") as handle:
    readme = handle.read()

setup(
    name="alchemymodel_xlsx",
    version="1.0.4",
    description="A library to management excel from SQLAlchemy queries.",
    packages=find_packages(exclude=["test", "test.*"]),
    long_description=readme,
    long_description_content_type="text/x-rst",
    python_requires=">=3.9",
    install_requires=[
        "XlsxWriter>=3.1.0",
        "openpyxl>=3.1.2",
        "pandas>=2.0.0",
        "numpy>=1.24.2",
        "SQLAlchemy>=1.4.47",
    ],
    url="https://github.com/GM4nn/alchemymodel_xlsx",
    author="German Alejandro Castellanos Marin",
    author_email="germal150@hotmail.com",
)
