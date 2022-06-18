import logging
from datetime import datetime
from typing import Generator, Optional, Union

import anypoint.vendor.mureq as requests
from anypoint import utils
from anypoint.http_client.client import HttpClient
from anypoint.models.application import Application
from anypoint.models.environment import Environment
from anypoint.models.organization import Organization
from anypoint.models.statistics import DashboardStatistics, Statistic
from anypoint.monitoring import MonitoringApi

_default_log = logging.getLogger(__name__)


class Anypoint:

    def __init__(self,
                 username: str,
                 password: str,
                 base_url: str = "https://anypoint.mulesoft.com",
                 log: logging.Logger = _default_log):
        self._username = username
        self._password = password
        self._log = log
        self._base_url = base_url
        self._access_token: Optional[str] = None
        # self.organization: Optional[Organization] = None

        self._http_client = HttpClient(log)

        self.monitoring_api = MonitoringApi(self)

    def login(self):
        path = "/accounts/login"
        r = self._request(path, "POST", {"username": self._username, "password": self._password})
        self._access_token = r.get("access_token")

    def me(self) -> dict:
        # TODO - Parse the response
        path = "/accounts/api/me"
        return self._request(path)

    def get_organization(self, org_id: Optional[str] = None) -> Organization:
        if org_id is None:
            data = self.me()
        else:
            path = f"/accounts/api/organizations/{org_id}"
            data = self._request(path)
        return Organization(data.get("user", {}).get("organization", {}), self)

    def get_environments(self, organization_id: str) -> Generator[Environment, None, None]:
        path = f"/accounts/api/organizations/{organization_id}/environments"
        data = self._request(path)
        for env in data.get("data", []):
            env["organization_id"] = organization_id
            yield Environment(env, self)

    def get_application_statistics(self,
                                   environment_id: str,
                                   app_domain: str,
                                   date_from: datetime,
                                   date_to: datetime) -> Generator[Statistic, None, None]:
        path = f"/cloudhub/api/applications/{app_domain}/statistics"
        headers = {"X-ANYPNT-ENV-ID": environment_id}
        params = {
            "start": f"{int(date_from.timestamp() * 1000)}",
            "end": f"{int(date_to.timestamp() * 1000)}",
            "intervalCount": f"{(date_to - date_from).total_seconds() // 60:0.0f}"
        }
        data = self._request(path, parameters=params, headers=headers)
        for timestamp, value in data.items():
            yield Statistic(timestamp, value)

    def get_application_dashboard_statistics(self,
                                             environment_id: str,
                                             app_domain: str,
                                             date_from: datetime,
                                             date_to: datetime) -> DashboardStatistics:
        path = f"/cloudhub/api/v2/applications/{app_domain}/dashboardStats"
        headers = {"X-ANYPNT-ENV-ID": environment_id}
        params = {
            "startDate": utils.date_to_str(date_from),
            "endDate": utils.date_to_str(date_to),
            "interval": "60000"
        }
        data = self._request(path, parameters=params, headers=headers)
        return DashboardStatistics(data)

    def get_applications(self, environment_id: str) -> Generator[Application, None, None]:
        path = f"/cloudhub/api/applications"
        headers = {"X-ANYPNT-ENV-ID": environment_id}
        data = self._request(path, headers=headers)
        for app in data:
            app["environment_id"] = environment_id
            yield Application(app, self)

    def get_apis(self, organization_id: str, environment_id: str) -> Generator[dict, None, None]:
        path = f"/apimanager/api/v1/organizations/{organization_id}/environments/{environment_id}/apis"
        data = self._request(path)
        for api in data.get("assets", []):
            yield api

    def _request(self, path: str,
                 method: str = "GET",
                 body: Optional[dict] = None,
                 headers: Optional[dict] = None,
                 parameters: Optional[dict] = None,
                 return_json = True) -> Union[dict, requests.Response]:
        url = f"{self._base_url}{path}"
        if not self._access_token and not url.endswith("/accounts/login"):
            self.login()
        if headers is None:
            headers = {}
        headers.update({
            "Authorization": f"Bearer {self._access_token}"
        })

        return self._http_client.request(url, method, body, headers, parameters, return_json)
