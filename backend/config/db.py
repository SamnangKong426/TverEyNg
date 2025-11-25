from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine


sqlite_file_name = "database/db.sqlite"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    # Only for development
    # SQLModel.metadata.drop_all(engine)  # drop all tables
    SQLModel.metadata.create_all(engine)  # recreate tables


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]