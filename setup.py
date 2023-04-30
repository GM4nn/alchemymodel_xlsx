from setuptools import find_packages, setup

setup(
    name="alchemymodel_xlsx",
    version="1.0.0",
    description="A library to management excel from SQLAlchemy queries.",
    packages=find_packages(exclude=["test", "test.*"]),
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
