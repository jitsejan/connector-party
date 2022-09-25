"""Definition of the Database."""
from sqlmodel import create_engine

SQLITE_FILE_NAME = "database.db"
SQLITE_URL = (
    f"sqlite:////Users/jitsejan/code/personal/connector-party/{SQLITE_FILE_NAME}"
)

engine = create_engine(SQLITE_URL, echo=True)
