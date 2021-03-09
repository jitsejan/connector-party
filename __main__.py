from jiraretriever import JiraRetriever
from schemas import JiraProject


def main() -> None:
    jr = JiraRetriever(project_key="DT")
    board = jr.get_board_for_project_key()
    sprints = jr.get_sprints_for_board(board)
    issues = jr.get_issues_for_project()
    print(sprints[0])
    print(issues[0])


if __name__ == "__main__":
    main()
