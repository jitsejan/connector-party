"""Contains examples for each of the retrievers."""
from connector_party.jiraretriever import JiraRetriever


def jira_example() -> None:
    """Example for Jira retrieval."""
    jira = JiraRetriever(project_key="DTT")
    frame = jira.get_issue_dataframe()
    print(frame)
    print(frame.dtypes)


if __name__ == "__main__":
    jira_example()
