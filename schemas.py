from dataclasses import dataclass
from datetime import datetime

@dataclass
class JiraBoard:
    """Class for the Jira Board."""

    id: int
    name: str
    project_key: str


@dataclass
class JiraProject:
    """Class for the Jira Project."""

    id: int
    key: str
    name: str


@dataclass
class JiraSprint:
    """ Class for the Jira Sprint."""

    board_id: int
    id : int
    name: str
    state: str
    start_date: datetime
    end_date: datetime
