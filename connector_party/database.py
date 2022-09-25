"""Definition of the Database."""
from sqlmodel import create_engine

sqlite_file_name = "database.db"
sqlite_url = (
    f"sqlite:////Users/jitsejan/code/personal/connector-party/{sqlite_file_name}"
)

engine = create_engine(sqlite_url, echo=True)
