from __future__ import annotations

import logging
import typing
from typing import List

from anypoint.models.api import Api

if typing.TYPE_CHECKING:
    from anypoint import Anypoint


class ApiManagerApi:
    def __init__(self, client: Anypoint, log: logging.Logger):
        self._client = client
        self._log = log

    def get_apis(self, organization_id: str, environment_id: str) -> List[Api]:
        path = f"/apimanager/api/v1/organizations/{organization_id}/environments/{environment_id}/apis"
        assets = self._client.request(path).get("assets", [])
        for asset in assets:
            yield from [Api(raw_data, self) for raw_data in asset.get("apis", [])]
