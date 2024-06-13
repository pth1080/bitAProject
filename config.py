import os


class Config:
    PG_HOST = os.getenv('POSTGRES_HOST')
    PG_DATABASE = os.getenv('POSTGRES_DB')
    PG_USER = os.getenv('POSTGRES_USER')
    PG_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    PG_PORT = os.getenv('POSTGRES_PORT')
    DATABASE_URL = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"
    DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
