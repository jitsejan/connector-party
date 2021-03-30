import pytest
from src.connector_party.jiraretriever import JiraRetriever

PROJECT_KEY = "DT"


class TestJiraRetriever:
    
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.subject = JiraRetriever(project_key=PROJECT_KEY)

    def test_instantiate(self):
        """ Test the instantiation """
        assert self.subject

    def test_return_something(self):
        result = self.subject.get_issue_dataframe()
        assert len(result) > 0
