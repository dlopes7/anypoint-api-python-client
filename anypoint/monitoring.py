import logging
from datetime import datetime
from typing import List, TYPE_CHECKING

from anypoint.utils import date_to_str

if TYPE_CHECKING:
    from anypoint import Anypoint


class MonitoringApi:
    def __init__(self, api_client: "Anypoint", log: logging.Logger):
        self._api_client = api_client
        self._log = log

    def get_applications(self, organization_id: str,
                         environment_id: str,
                         date_from: datetime,
                         date_to: datetime,
                         app_ids: List[str],
                         detailed: bool = True):
        path = f"/monitoring/query/api/v1/organizations/{organization_id}/environments/{environment_id}/applications"
        params = {
            "from": date_to_str(date_from),
            "to": date_to_str(date_to),
            "detailed": detailed
        }
        body = {
            "ids": app_ids
        }
        return self._api_client.request(path, method="POST", parameters=params, body=body)

    def get_application(self, organization_id: str,
                        environment_id: str,
                        date_from: datetime,
                        date_to: datetime,
                        app_id: str,
                        detailed: bool = True):
        path = f"/monitoring/query/api/v1/organizations/{organization_id}/environments/" \
               f"{environment_id}/applications/{app_id}"
        params = {
            "from": date_to_str(date_from),
            "to": date_to_str(date_to),
            "detailed": detailed
        }
        return self._api_client.request(path, parameters=params)
