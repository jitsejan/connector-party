from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, PositiveInt


class JiraBoard(BaseModel):
    """Class for a Jira Board."""

    id: int
    name: str
    project_key: str


class JiraHistory(BaseModel):
    """Class for a Jira history item."""

    author: str
    created: datetime
    field: str
    old: Optional[str]
    new: Optional[str]


class JiraIssue(BaseModel):
    """Class for a Jira Issue."""

    id: PositiveInt
    key: str = Field(regex=r"^[\w]*-[\d]*$")
    description: Optional[str]
    summmary: Optional[str]
    estimate: Optional[str]
    histories: Optional[List[JiraHistory]]
    project: Optional[str]
    sprint: Optional[str]


class JiraProject(BaseModel):
    """Class for a Jira Project."""

    id: PositiveInt
    key: str
    name: str


class JiraSprint(BaseModel):
    """ Class for a Jira Sprint."""

    board_id: PositiveInt
    id: PositiveInt
    name: str
    state: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    complete_date: Optional[datetime]
