import os
from typing import Dict, List, Optional, Union

import pandas as pd
from pandas import DataFrame  # type: ignore
from requests import Session
from requests.auth import HTTPBasicAuth
from requests.structures import CaseInsensitiveDict

from .schemas import JiraBoard, JiraHistory, JiraIssue, JiraProject, JiraSprint


class JiraRetriever:
    """Class to retrieve data from Jira."""

    MAX_RESULTS = 100
    ESTIMATE_FIELD = "customfield_11715"

    def __init__(self, project_key: str):
        """Initialize the Jira retriever."""
        self._project_key = project_key
        self._session = self._get_session()
        self._boards = self._get_boards()
        self._projects = self._get_projects()
        self._project = self.get_project_for_project_key()

    def _get_session(self) -> Session:
        session = Session()
        session.headers = self.headers
        session.auth = HTTPBasicAuth(self.user, self.api_key)
        return session

    def _get_dataframe(self, inputlist: List) -> DataFrame:
        return DataFrame([i.dict() for i in inputlist])

    def _get_num_results(self, url: str) -> int:
        params = {"maxResults": 0}
        response = self._get_json_data_for_url(url, params)
        return response.get("total", 1)

    def _get_json_data_for_url(self, url: str, params: Dict = {}) -> Dict:
        return self.session.get(url=url, params=params).json()

    def _get_paginated_json_data(
        self, url: str, key: str = "values", extra_params: dict = {}
    ) -> List[Dict]:
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
        assignee = item["fields"].get("assignee")
        if assignee:
            return assignee.get("displayName")
        return None

    def _get_boards(self) -> List[JiraBoard]:
        url = f"{self.url}/rest/agile/1.0/board"
        return [
            JiraBoard(
                id=int(item["id"]),
                name=item["name"],
                project_key=item["location"]["projectKey"],
            )
            for item in self._get_paginated_json_data(url=url)
        ]

    def _get_projects(self) -> List[JiraProject]:
        url = f"{self.url}/rest/api/3/project/search"
        return [
            JiraProject(id=int(item["id"]), key=item["key"], name=item["name"])
            for item in self._get_paginated_json_data(url=url)
        ]

    def get_board_for_project_key(
        self, project_key: str = None
    ) -> Union[JiraBoard, None]:
        if not project_key:
            project_key = self.project_key
        return next((b for b in self.boards if b.project_key == project_key), None)

    def get_project_for_project_key(
        self, project_key: str = None
    ) -> Union[JiraProject, None]:
        if not project_key:
            project_key = self.project_key
        return next((p for p in self.projects if p.key == project_key), None)

    @classmethod
    def _convert_histories(cls, item: Dict) -> List[JiraHistory]:
        try:
            histories = item["changelog"]["histories"]
        except Exception:
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
        extra_params = {"expand": "changelog"}
        if not project:
            project = self.project
        url = f"{self.url}/rest/api/2/search?jql=project={project.key}"
        return [
            JiraIssue(
                id=item["id"],
                key=item["key"],
                assignee=self._get_assignee(item),
                issuetype=item["fields"]["issuetype"]["name"],
                description=item["fields"]["description"],
                created=item["fields"]["created"],
                updated=item["fields"]["updated"],
                summary=item["fields"]["summary"],
                estimate=item["fields"][self.ESTIMATE_FIELD],
                histories=self._convert_histories(item),
                project=project.key,
                status=item["fields"]["status"]["name"],
            )
            for item in self._get_paginated_json_data(
                url=url, key="issues", extra_params=extra_params
            )
        ]

    def get_issue_frame_for_project(self, project: JiraProject = None) -> DataFrame:
        return DataFrame([i.dict() for i in self.get_issues_for_project(project)])

    def get_issues_for_sprint(self, sprint: JiraSprint) -> List[JiraIssue]:
        extra_params = {"expand": "changelog"}
        url = f"{self.url}/rest/agile/1.0/sprint/{sprint.id}/issue"
        return [
            JiraIssue(
                id=item["id"],
                key=item["key"],
                assignee=self._get_assignee(item),
                issuetype=item["fields"]["issuetype"]["name"],
                description=item["fields"]["description"],
                created=item["fields"]["created"],
                updated=item["fields"]["updated"],
                summary=item["fields"]["summary"],
                estimate=item["fields"][self.ESTIMATE_FIELD],
                histories=self._convert_histories(item),
                project=item["fields"]["project"]["key"],
                sprint=sprint.name,
                status=item["fields"]["status"]["name"],
            )
            for item in self._get_paginated_json_data(
                url=url, key="issues", extra_params=extra_params
            )
        ]

    def get_sprints_for_board(self, board: JiraBoard) -> List[JiraSprint]:
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
            )
            for item in self._get_paginated_json_data(url=url)
        ]

    def get_issues_for_all_sprints(self) -> List[JiraIssue]:
        board = self.get_board_for_project_key()
        sprints = self.get_sprints_for_board(board=board)
        result = []
        for sprint in sprints:
            result.extend(self.get_issues_for_sprint(sprint=sprint))
        return result

    def get_issue_dataframe(self) -> DataFrame:
        frame = self._get_dataframe(self.get_issues_for_all_sprints())
        if not frame.empty:
            for col in ["created", "updated"]:
                frame[col] = pd.to_datetime(frame[col], utc=True)
        return frame

    @property
    def api_key(self) -> Optional[str]:
        return os.getenv("JIRA_API_KEY")

    @property
    def boards(self) -> List[JiraBoard]:
        return self._boards

    @property
    def headers(self) -> CaseInsensitiveDict:
        return CaseInsensitiveDict({"Accept": "application/json"})

    @property
    def project_key(self) -> str:
        return self._project_key

    @property
    def project(self) -> JiraProject:
        return self._project

    @property
    def projects(self) -> List[JiraProject]:
        return self._projects

    @property
    def session(self) -> Session:
        return self._session

    @property
    def url(self) -> Optional[str]:
        return os.getenv("JIRA_URL")

    @property
    def user(self) -> Optional[str]:
        return os.getenv("JIRA_USER")
