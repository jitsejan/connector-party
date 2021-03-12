import pandas as pd  # type: ignore

from jiraretriever import JiraRetriever


def main() -> None:
    jr = JiraRetriever(project_key="DT")
    board = jr.get_board_for_project_key()
    sprints = jr.get_sprints_for_board(board)
    all_issues_by_sprint = []
    for sprint in sprints:
        issues = jr.get_issues_for_sprint(sprint)
        all_issues_by_sprint.extend(issues)
    df = pd.DataFrame([s.dict() for s in all_issues_by_sprint])
    print(df.tail(10))


if __name__ == "__main__":
    main()
