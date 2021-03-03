from jiraretriever import JiraRetriever
from schemas import JiraProject


def main():
    jr = JiraRetriever(project_key="DT")
    # Perhaps enable when `project_key` is not defined and a user prompt
    # is needed.
    # projects = jr.get_projects()
    # print(projects)
    board = jr.get_board_for_project_key()
    print(board.id)
    print(jr.get_sprints_for_board(board))

if __name__ == "__main__":
    main()
