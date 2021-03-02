from jiraretriever import JiraRetriever
from schemas import JiraProject

def main():
    jr = JiraRetriever(project="DT")
    projects = jr.get_projects()
    print(projects)

if __name__ == "__main__":
    main()
