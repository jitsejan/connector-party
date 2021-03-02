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
