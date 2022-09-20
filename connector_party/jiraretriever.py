"""Definition of the JiraRetriever class."""
import os
from typing import Dict, List, Optional, Union

import pandas as pd
from pandas import DataFrame
from requests import Session
from requests.auth import HTTPBasicAuth
from requests.structures import CaseInsensitiveDict

from .schemas import JiraBoard, JiraHistory, JiraIssue, JiraProject, JiraSprint


class JiraRetriever:
    """Class to retrieve data from Jira."""

    MAX_RESULTS = 50

    def __init__(self, project_key: str, sprint_field: str = None):
        """Initialize the Jira retriever."""
        self._project_key = project_key
        self._sprint_field = sprint_field
        self._session = self._get_session()
        self._boards = self._get_boards()
        self._projects = self._get_projects()
        self._project = self.get_project_for_project_key()
        board = self.get_board_for_project_key()
        self._sprints = self.get_sprints_for_board(board=board)

    def _get_session(self) -> Session:
        """Return a session with headers and auth set."""
        session = Session()
        session.headers = self.headers
        session.auth = HTTPBasicAuth(self.user, self.api_key)
        return session

    def _get_dataframe(self, inputlist: List) -> DataFrame:
        """Return a dataframe converting the issues."""
        return DataFrame([i.dict() for i in inputlist])

    def _get_num_results(self, url: str) -> int:
        """Return the number of total results."""
        params = {"maxResults": 0}
        response = self._get_json_data_for_url(url, params)
        return response.get("total", 1)

    def _get_json_data_for_url(self, url: str, params=None) -> Dict:
        """Return JSON data for a given url and its parameters."""
        if params is None:
            params = {}
        return self.session.get(url=url, params=params).json()

    def _get_paginated_json_data(
        self, url: str, key: str = "values", extra_params=None
    ) -> List[Dict]:
        """Return the JSON data for a paginated page."""
        if extra_params is None:
            extra_params = {}
        num_results = self._get_num_results(url=url)
        result_list = []
        params = {
            "maxResults": self.MAX_RESULTS,
            "startAt": 0,
        }
        params = params | extra_params
        for start in range(0, num_results, self.MAX_RESULTS):
            params.update(
                {
                    "startAt": start,
                }
            )
            response = self._get_json_data_for_url(url=url, params=params)
            result_list.extend(response[key])
        return result_list

    def _get_assignee(self, item: Dict) -> Union[str, None]:
        """Return the assignee if it is set."""
        if (
            "assignee" in item["versionedRepresentations"].keys()
            and item["versionedRepresentations"]["assignee"]["1"] is not None
        ):
            return item["versionedRepresentations"]["assignee"]["1"]["displayName"]
        return None

    def _get_boards(self) -> List[JiraBoard]:
        """Return a list of Jira boards."""
        url = f"{self.url}/rest/agile/1.0/board"
        return [
            JiraBoard(
                id=int(item["id"]),
                name=item["name"],
                project_key=self._get_project_key_for_item(item),
            )
            for item in self._get_paginated_json_data(url=url)
        ]

    def _get_projects(self) -> List[JiraProject]:
        """Return a list of Jira projects."""
        url = f"{self.url}/rest/api/2/project/search"
        return [
            JiraProject(id=int(item["id"]), key=item["key"], name=item["name"])
            for item in self._get_paginated_json_data(url=url)
        ]

    def get_board_for_project_key(self, project_key: str = None) -> JiraBoard:
        """Return the board for a given project key."""
        if not project_key:
            project_key = self.project_key
        return next(b for b in self.boards if b.project_key == project_key)

    def get_project_for_project_key(self, project_key: str = None) -> JiraProject:
        """Return the project for a given project key."""
        if not project_key:
            project_key = self.project_key
        return next(p for p in self.projects if p.key == project_key)

    def _get_sprints(self, item: dict) -> List[int]:
        sprints = []
        if (
            self.sprint_field
            and item["versionedRepresentations"][self.sprint_field] is not None
        ):
            for key in item["versionedRepresentations"].get(self.sprint_field):
                if (
                    item["versionedRepresentations"].get(self.sprint_field).get(key)
                    is not None
                ):
                    for sprint in (
                        item["versionedRepresentations"].get(self.sprint_field).get(key)
                    ):
                        sprints.append(sprint.get("id"))
        return sprints

    @classmethod
    def _convert_histories(cls, item: Dict) -> List[JiraHistory]:
        """Convert a dictionary to a list of Jira History items."""
        try:
            histories = item["changelog"]["histories"]
        except KeyError:
            return []
        else:
            return [
                JiraHistory(
                    author=h["author"]["displayName"],
                    created=h["created"],
                    field=elem["field"],
                    old=elem["fromString"],
                    new=elem["toString"],
                )
                for h in histories
                for elem in h["items"]
            ]

    def get_issues_for_project(self, project: JiraProject = None) -> List[JiraIssue]:
        """Return a list of Jira issues for a given Jira project."""
        extra_params = {"expand": "changelog,versionedRepresentations,renderedFields"}
        if not project:
            project = self.project
        url = f"{self.url}/rest/api/2/search?jql=project={project.key}"
        return [
            JiraIssue(
                id=item["id"],
                key=item["key"],
                assignee=self._get_assignee(item),
                issuetype=item["versionedRepresentations"]["issuetype"]["1"]["name"],
                description=item["versionedRepresentations"]["description"]["1"],
                created=item["versionedRepresentations"]["created"]["1"],
                updated=item["versionedRepresentations"]["updated"]["1"],
                summary=item["versionedRepresentations"]["summary"]["1"],
                # histories=self._convert_histories(item), # TODO Move to own table
                sprints=self._get_sprints(item),
                project=project.key,
                status=item["versionedRepresentations"]["status"]["1"]["name"],
            )
            for item in self._get_paginated_json_data(
                url=url, key="issues", extra_params=extra_params
            )
        ]

    def get_issue_frame_for_project(self, project: JiraProject = None) -> DataFrame:
        """Return a dataframe with Jira issues for a given Jira project."""
        return self._get_dataframe(self.get_issues_for_project(project=project))

    def get_sprints_for_board(self, board: JiraBoard) -> List[JiraSprint]:
        """Return the sprints for a given Jira board."""
        url = f"{self.url}/rest/agile/1.0/board/{board.id}/sprint"
        return [
            JiraSprint(
                board_id=item["originBoardId"],
                id=item["id"],
                name=item["name"],
                state=item["state"],
                start_date=item["startDate"],
                end_date=item["endDate"],
                complete_date=item.get("completeDate"),
                goal=item.get("goal"),
            )
            for item in self._get_paginated_json_data(url=url)
        ]

    def get_issue_dataframe(self) -> DataFrame:
        """Return a dataframe with Jira issues."""
        frame = self.get_issue_frame_for_project(project=self.project)
        if not frame.empty:
            for col in ["created", "updated"]:
                frame[col] = pd.to_datetime(frame[col], utc=True)
        return frame

    def get_sprint_dataframe(self) -> DataFrame:
        """Return a dataframe with Jira sprints."""
        frame = self._get_dataframe(self.sprints)
        if not frame.empty:
            for col in ["start_date", "end_date", "complete_date"]:
                frame[col] = pd.to_datetime(frame[col], utc=True)
        return frame

    @staticmethod
    def _get_project_key_for_item(item: dict) -> str:
        try:
            return item["location"]["projectKey"]
        except KeyError:
            return ""

    @property
    def api_key(self) -> Optional[str]:
        """Return API key to access Jira."""
        return os.getenv("JIRA_API_KEY")

    @property
    def boards(self) -> List[JiraBoard]:
        """Return list of Jira boards."""
        return self._boards

    @property
    def headers(self) -> CaseInsensitiveDict:
        """Return headers for the API requests."""
        return CaseInsensitiveDict({"Accept": "application/json"})

    @property
    def project_key(self) -> str:
        """Return project key to access the Jira issues."""
        return self._project_key

    @property
    def project(self) -> JiraProject:
        """Return the Jira project."""
        return self._project

    @property
    def projects(self) -> List[JiraProject]:
        """Return list of Jira projects."""
        return self._projects

    @property
    def session(self) -> Session:
        """Return session to execute Jira API calls."""
        return self._session

    @property
    def sprint_field(self) -> str:
        """Return sprint field within the Jira issues."""
        return self._sprint_field

    @property
    def sprints(self) -> List[JiraSprint]:
        """Return list of Jira projects."""
        return self._sprints

    @property
    def url(self) -> Optional[str]:
        """Return URL for the Jira instance."""
        return os.getenv("JIRA_URL")

    @property
    def user(self) -> Optional[str]:
        """Return user to access Jira."""
        return os.getenv("JIRA_USER")
