from pydantic import BaseModel
from datetime import datetime


class JiraBoard(BaseModel):
    """Class for the Jira Board."""

    id: int
    name: str
    project_key: str


class JiraProject(BaseModel):
    """Class for the Jira Project."""

    id: int
    key: str
    name: str


class JiraSprint(BaseModel):
    """ Class for the Jira Sprint."""

    board_id: int
    id: int
    name: str
    state: str
    start_date: datetime
    end_date: datetime
    complete_date: datetime = None
