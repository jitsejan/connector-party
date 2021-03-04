from jiraretriever import JiraRetriever
from schemas import JiraProject


def main() -> None:
    jr = JiraRetriever(project_key="DT")
    # Perhaps enable when `project_key` is not defined and a user prompt
    # is needed.
    # projects = jr.get_projects()
    # print(projects)
    # board = jr.get_board_for_project_key()
    # print(board)
    # print(jr.get_sprints_for_board(board))
    print(jr.project)
    issues = jr.get_issues_for_project()
    print(issues[0])

if __name__ == "__main__":
    main()
