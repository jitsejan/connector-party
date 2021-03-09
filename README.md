# connector-party

This repository contains connectors for third parties.

- Jira

## Usage

### Jira Retriever

Make sure to have the following environment variables set in your terminal. Obviously change with the correct values. Get the API key from the Atlassian [website](https://id.atlassian.com/manage-profile/security/api-tokens).

```bash
export JIRA_API_KEY=MyApIk3y
export JIRA_URL=https://jitsejan.atlassian.net
export JIRA_USER=jira@jitsejan.com
```

To use the Jira retriever you will need to provide the project name.

```python
from jiraretriever import JiraRetriever

jr = JiraRetriever(project="DATA")

```

The retriever currently has an interface to return **sprints** and **issues**. Note that for the sprints retrieval a board needs to be provided. For the issues it will assume the project that is used in the initialization of the class.

```python
board = jr.get_board_for_project_key()
sprints = jr.get_sprints_for_board(board)
issues = jr.get_issues_for_project()
```

## Personal objectives

- Learn how to make a Python package and use that package in a different repository
- Improve my knowledge on Pydantic and type hinting
