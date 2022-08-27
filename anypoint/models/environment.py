from typing import Generator, List, TYPE_CHECKING

from anypoint.models.application import Application

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
