"""Definitions of the different schemas used by the retrievers."""

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
    assignee: Optional[str]
    issuetype: str
    created: datetime
    updated: datetime
    description: Optional[str]
    summary: Optional[str]
    estimate: Optional[str]
    histories: Optional[List[JiraHistory]]
    project: Optional[str]
    sprints: Optional[List[str]]
    status: str


class JiraProject(BaseModel):
    """Class for a Jira Project."""

    id: PositiveInt
    key: str
    name: str


class JiraSprint(BaseModel):
    """Class for a Jira Sprint."""

    board_id: PositiveInt
    id: PositiveInt
    name: str
    state: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    complete_date: Optional[datetime]
    goal: str
