POSTGRES_DB = "db_sqlmodel_xlsx"
POSTGRES_PASSWORD = "admin"
POSTGRES_PORT = 5432
POSTGRES_SERVER = "localhost"
POSTGRES_USER = "postgres"
SQLALCHEMY_DATABASE_URI = (
    f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}'
    f':{POSTGRES_PORT}/{POSTGRES_DB}'
)
