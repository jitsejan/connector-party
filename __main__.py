from jiraretriever import JiraRetriever
from schemas import JiraProject


def main():
    jr = JiraRetriever(project="DT")
    # Perhaps enable when `project` is not defined and a user prompt
    # is needed.
    # projects = jr.get_projects()
    # print(projects)
    boards = jr.get_boards()
    print(boards)


if __name__ == "__main__":
    main()
