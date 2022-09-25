"""Contains the test for the JiraRetriever class."""
import pytest

from connector_party.jiraretriever import JiraRetriever

PROJECT_KEY = "INVDP"


class TestJiraRetriever:
    """Defines the test class for the JiraRetriever."""

    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Set up the test class."""
        self.subject = JiraRetriever(project_key=PROJECT_KEY)

    def test_instantiate(self):
        """Test the instantiation of the JiraRetriever."""
        assert self.subject

    # def test_fields_are_present(self):
    #     """Test expected fields are present in columns."""
    #     result = self.subject.get_issue_dataframe()
    #
    #     assert "assignee" in result.columns
    #     assert "status" in result.columns
    #     assert "created" in result.columns
    #     assert "updated" in result.columns
