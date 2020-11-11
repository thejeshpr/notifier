import os

import databases
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_PORT = os.environ.get("DB_PORT")
ENV = os.environ.get("ENV")


# SQLALCHEMY_DATABASE_URL = os.getenv("DB_CONN", "sqlite:///dev8.db?check_same_thread=False")

# # SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"



# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()


# # only for SQLITE
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# # for postgres
# # engine = create_engine(SQLALCHEMY_DATABASE_URL)


# # async db cursor
# # ASYNC_DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
# ASYNC_DB_URL = SQLALCHEMY_DATABASE_URL

# db_cursor = databases.Database(ASYNC_DB_URL)


if ENV == "PROD":
    SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    ASYNC_DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

else:
    SQLALCHEMY_DATABASE_URL = os.getenv("DB_CONN", "sqlite:///dev8.db?check_same_thread=False")
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})    
    ASYNC_DB_URL = SQLALCHEMY_DATABASE_URL



# Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_cursor = databases.Database(ASYNC_DB_URL)