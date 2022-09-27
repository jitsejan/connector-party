"""Contains examples for each of the retrievers."""
from sqlmodel import Session, SQLModel, select

from connector_party.database import engine
from connector_party.jiraretriever import JiraRetriever
from connector_party.schemas import JiraBoard, JiraProject, JiraSprint


def jira_example() -> JiraRetriever:
    """Run example for Jira retrieval."""
    return JiraRetriever(project_key="INVDP")


def create_db_and_tables():
    """Create the tables for the Jira retriever."""
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    """Main function."""
    create_db_and_tables()
    with Session(engine) as session:
        jira = jira_example()
        for board in jira.boards:
            result = session.exec(
                select(JiraBoard).where(JiraBoard.id == board.id)
            ).first()
            if result is None:
                session.add(board)
        for project in jira.projects:
            result = session.exec(
                select(JiraProject).where(JiraProject.id == project.id)
            ).first()
            if result is None:
                session.add(project)
        for sprint in jira.sprints:
            result = session.exec(
                select(JiraSprint).where(JiraSprint.id == sprint.id)
            ).first()
            if result is None:
                session.add(sprint)
        issues = jira.get_issues_for_project()
        print(len(issues))
        session.commit()
