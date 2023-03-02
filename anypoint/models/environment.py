from typing import Generator, List, TYPE_CHECKING

from anypoint.models.api import Asset
from anypoint.models.application import Application
from anypoint.models.destination import Destination, Queue

if TYPE_CHECKING:
    from anypoint import Anypoint


class Environment:
    def __init__(self, raw_json, client: "Anypoint"):
        self.id: str = raw_json.get("id")
        self.name: str = raw_json.get("name")
        self.is_production: bool = raw_json.get("isProduction")
        self.type: str = raw_json.get("type")
        self.client_id: str = raw_json.get("clientId")
        self.organization_id = raw_json.get("organizationId")
        self.applications: List[Application] = []

        self._data = raw_json
        self._client = client

    def __repr__(self):
        return f"Environment({self.name}, {self.id})"

    def get_applications(self) -> Generator[Application, None, None]:
        return self._client.applications.get_applications(self.id)

    def get_apis(self) -> List[Asset]:
        return self._client.api_manager.get_apis(self.organization_id, self.id)

    def get_organization(self):
        return self._client.organizations.get_environment_organization(self.id)

    def get_mq_queues(self, region_id: str, destinations: List[str] = None):
        return self._client.mq.get_queues(self.organization_id, self.id, region_id, destinations)

    def get_mq_queue(self, region_id: str, destination_id: str) -> Queue:
        return self._client.mq.get_queue(self.organization_id, self.id, region_id, destination_id)

    def get_mq_destinations(self, region_id: str) -> List[Destination]:
        return self._client.mq.get_destinations(self.organization_id, self.id, region_id)
