from jiraretriever import JiraRetriever


def main():
    jr = JiraRetriever(project="DT")
    print(jr.project)


if __name__ == "__main__":
    main()
