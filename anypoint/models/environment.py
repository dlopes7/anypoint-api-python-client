from datetime import datetime
from typing import List, TYPE_CHECKING

from anypoint.models.application import Application

if TYPE_CHECKING:
    from anypoint import Anypoint


class Environment:
    def __init__(self, raw_json, client: "Anypoint"):
        self.id: str = raw_json["id"]
        self.name: str = raw_json["name"]
        self.is_production: bool = raw_json["isProduction"]
        self.type: str = raw_json["type"]
        self.client_id: str = raw_json["clientId"]
        self.organization_id = raw_json.get("organizationId")
        self.applications: List[Application] = []

        self._data = raw_json
        self._api_client = client

    def __repr__(self):
        return f"Environment({self.name}, {self.id})"

    def get_monitoring_applications(self, date_from: datetime, date_to: datetime, app_ids: List[str],
                                    detailed: bool = True):
        return self._api_client.monitoring_api.get_applications(self.organization_id,
                                                                self.id,
                                                                date_from,
                                                                date_to,
                                                                app_ids,
                                                                detailed)

    def get_monitoring_application(self, date_from: datetime, date_to: datetime, app_id: str, detailed: bool = True):
        return self._api_client.monitoring_api.get_application(self.organization_id,
                                                               self.id,
                                                               date_from,
                                                               date_to,
                                                               app_id,
                                                               detailed)

    def get_applications(self):
        return self._api_client.get_applications(self.id)

    def get_apis(self):
        return self._api_client.get_apis(self.organization_id, self.id)
