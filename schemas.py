from dataclasses import dataclass


@dataclass
class JiraProject:
    """Class for the Jira Project."""

    id: int
    key: str
    name: str
