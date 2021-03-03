from dataclasses import dataclass


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
