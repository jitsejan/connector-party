from connector_party.jiraretriever import JiraRetriever


def main() -> None:
    jr = JiraRetriever(project_key="DTT")
    df = jr.get_issue_dataframe()
    print(df)
    print(df.dtypes)


if __name__ == "__main__":
    main()
