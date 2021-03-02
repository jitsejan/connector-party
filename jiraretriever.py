import os
from requests import Session
from requests.auth import HTTPBasicAuth

from typing import Dict

class JiraRetriever:

    def __init__(self, project: str):
        self._project = project
        self._session = self._get_session()
        
    def _get_session(self) -> Session:
        session = Session()
        session.headers = self.headers
        session.auth = HTTPBasicAuth(self.user, self.api_key)
        return session
    
    @property
    def api_key(self) -> str:
        return os.getenv("JIRA_API_KEY")

    @property
    def headers(self) -> Dict:
        return {
           "Accept": "application/json"
        }

    @property
    def project(self) -> str:
        return self._project

    @property
    def user(self) -> str:
        return os.getenv("JIRA_USER")
 