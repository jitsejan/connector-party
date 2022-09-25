"""Definitions of the different schemas used by the retrievers."""
from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class JiraIssueSprintLink(SQLModel, table=True):
    """Class for the link between Jira Issue and Sprint."""

    issue_id: Optional[int] = Field(
        default=None, foreign_key="jiraissue.id", primary_key=True
    )
    sprint_id: Optional[int] = Field(
        default=None, foreign_key="jirasprint.id", primary_key=True
    )


class JiraBoard(SQLModel, table=True):
    """Class for a Jira Board."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    project_key: str


class JiraHistory(SQLModel, table=False):
    """Class for a Jira history item."""

    author: str
    created: datetime
    field: str
    old: Optional[str]
    new: Optional[str]


class JiraIssue(SQLModel, table=True):
    """Class for a Jira Issue."""

    id: Optional[int] = Field(default=None, primary_key=True)
    key: str = Field(regex=r"^[\w]*-[\d]*$")
    assignee: Optional[str]
    issuetype: str
    created: datetime
    updated: datetime
    description: Optional[str]
    summary: Optional[str]
    estimate: Optional[str]
    # histories: Optional[List[JiraHistory]]
    # project: Optional[str] = Relationship(back_populates="jira")
    status: str

    sprints: List["JiraSprint"] = Relationship(
        back_populates="issues", link_model=JiraIssueSprintLink
    )


class JiraProject(SQLModel, table=True):
    """Class for a Jira Project."""

    id: Optional[int] = Field(default=None, primary_key=True)
    key: str
    name: str
    # issues: List[""]


class JiraSprint(SQLModel, table=True):
    """Class for a Jira Sprint."""

    id: Optional[int] = Field(default=None, primary_key=True)
    board_id: int
    name: str
    state: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    complete_date: Optional[datetime]
    goal: str

    issues: List["JiraIssue"] = Relationship(
        back_populates="sprints", link_model=JiraIssueSprintLink
    )
