import os
from typing import Dict, List, Optional

from requests import Session
from requests.auth import HTTPBasicAuth
from requests.structures import CaseInsensitiveDict

from schemas import JiraBoard, JiraProject


class JiraRetriever:
    MAX_RESULTS = 100

    def __init__(self, project: str):
        self._project = project
        self._session = self._get_session()

    def _get_session(self) -> Session:
        session = Session()
        session.headers = self.headers
        session.auth = HTTPBasicAuth(self.user, self.api_key)
        return session

    def _get_num_results(self, url: str) -> int:
        params = {"MaxResults": 0}
        response = self._get_json_data_for_url(url, params)
        return response["total"]

    def _get_json_data_for_url(self, url: str, params: Dict = {}) -> Dict:
        return self.session.get(url=url, params=params).json()

    def _get_paginated_json_data(self, url: str) -> List[Dict]:
        num_results = self._get_num_results(url=url)
        result_list = []
        params = {
            "maxResults": self.MAX_RESULTS,
            "startAt": 0,
        }
        for start in range(0, num_results, self.MAX_RESULTS):
            params.update(
                {
                    "startAt": start,
                }
            )
            response = self._get_json_data_for_url(url=url, params=params)
            result_list.extend(response["values"])
        return result_list

    def get_boards(self):
        url = f"{self.url}/rest/agile/1.0/board"
        return [
            JiraBoard(
                id=int(item["id"]),
                name=item["name"],
                project_key=item["location"]["projectKey"],
            )
            for item in self._get_paginated_json_data(url=url)
        ]

    def get_projects(self) -> List[JiraProject]:
        url = f"{self.url}/rest/api/3/project/search"
        return [
            JiraProject(id=int(item["id"]), key=item["key"], name=item["name"])
            for item in self._get_paginated_json_data(url=url)
        ]

    @property
    def api_key(self) -> Optional[str]:
        return os.getenv("JIRA_API_KEY")

    @property
    def headers(self) -> CaseInsensitiveDict:
        return CaseInsensitiveDict({"Accept": "application/json"})

    @property
    def project(self) -> str:
        return self._project

    @property
    def session(self) -> Session:
        return self._session

    @property
    def url(self) -> str:
        return os.getenv("JIRA_URL")

    @property
    def user(self) -> Optional[str]:
        return os.getenv("JIRA_USER")
