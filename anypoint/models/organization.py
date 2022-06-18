from typing import List, TYPE_CHECKING

from anypoint.models.environment import Environment

if TYPE_CHECKING:
    from anypoint import Anypoint


class Organization:
    def __init__(self, raw_json, client: "Anypoint"):
        self.id: str = raw_json["id"]
        self.name: str = raw_json["name"]

        self._data = raw_json
        self._api_client = client

    def get_environments(self) -> List[Environment]:
        return list(self._api_client.get_environments(self.id))
