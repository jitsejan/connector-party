import pytest

from connector_party.jiraretriever import JiraRetriever

PROJECT_KEY = "DTT"


class TestJiraRetriever:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.subject = JiraRetriever(project_key=PROJECT_KEY)

    def test_instantiate(self):
        """ Test the instantiation """
        assert self.subject

    def test_fields_are_prestent(self):
        result = self.subject.get_issue_dataframe()

        assert "assignee" in result.columns
        assert "status" in result.columns
        assert "created" in result.columns
        assert "updated" in result.columns
