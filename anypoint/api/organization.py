import logging
from typing import Generator, Optional, TYPE_CHECKING

from anypoint.models.environment import Environment
from anypoint.models.organization import Organization

if TYPE_CHECKING:
    from anypoint import Anypoint


class OrganizationApi:
    def __init__(self, client: "Anypoint", log: logging.Logger):
        self._client = client
        self._log = log

    def get_organization(self, org_id: Optional[str] = None) -> Organization:
        if org_id is None:
            data = self._client.me()
            data = data.get("user", {}).get("organization", {})
        else:
            path = f"/accounts/api/organizations/{org_id}"
            data = self._client.request(path)
        return Organization(data, self)

    def get_environments(self, organization_id: str) -> Generator[Environment, None, None]:
        path = f"/accounts/api/organizations/{organization_id}/environments"
        data = self._client.request(path)
        for env in data.get("data", []):
            env["organization_id"] = organization_id
            yield Environment(env, self._client)

    def get_environment_organization(self, environment_id: str) -> Organization:
        path = f"/cloudhub/api/organization"
        headers = {"X-ANYPNT-ENV-ID": environment_id}
        data = self._client.request(path, headers=headers)
        return Organization(data, self)
