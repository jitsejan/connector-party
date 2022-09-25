"""Contains examples for each of the retrievers."""
from sqlmodel import SQLModel

from connector_party.database import engine
from connector_party.jiraretriever import JiraRetriever


def jira_example() -> None:
    """Run example for Jira retrieval."""
    jira = JiraRetriever(project_key="INVDP")
    frame = jira.get_issue_dataframe()
    print(frame)
    print(frame.dtypes)


def create_db_and_tables():
    """Create the tables for the Jira retriever."""
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    """Main function."""
    create_db_and_tables()
    jira_example()
