import logging
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from anypoint.models.destination import Destination, Queue

if TYPE_CHECKING:
    from anypoint import Anypoint

# Fri, 11 Jul 2015 08:49:37 GMT
DATE_FORMAT = "%a, %d %b %Y %H:%M:%S %Z"


class MQApi:

    def __init__(self, anypoint: "Anypoint", log: logging.Logger):
        self._client = anypoint
        self._log = log

    def get_destinations(self, organization_id: str, environment_id: str, region: str) -> List[Destination]:
        #  https://anypoint.mulesoft.com/mq/admin/api/v1/organizations/{organizationId}/environments/{environmentId}/regions/{regionId}/destinations
        path = f"/mq/admin/api/v1/organizations/{organization_id}/environments/{environment_id}/regions/{region}/destinations"
        data = self._client.request(path)
        return [Destination(d, self._client, organization_id, environment_id, region) for d in data]

    def get_queues(self, organization_id: str, environment_id: str, region: str, destinations: List[str]):
        # curl -X GET "https://anypoint.mulesoft.com/mq/stats/api/v1/organizations/ORGANIZATION_ID/environments/ENVIRONMENT_ID/regions/REGION_URL/queues?destinationIds=DESTINATION_ID" \
        path = f"/mq/stats/api/v1/organizations/{organization_id}/environments/{environment_id}/regions/{region}/queues"
        params = {
            "destinationIds": ",".join(destinations) if destinations else None
        }
        return self._client.request(path, parameters=params)

    def get_queue(self,
                  organization_id: str,
                  environment_id: str,
                  region: str,
                  destination_id: str,
                  start_date: Optional[datetime] = None,
                  end_date: Optional[datetime] = None) -> Queue:
        path = f"/mq/stats/api/v1/organizations/{organization_id}/environments/{environment_id}/regions/{region}/queues/{destination_id}"
        params = {
            "startDate": start_date.strftime(DATE_FORMAT) if start_date else None,
            "endDate": end_date.strftime(DATE_FORMAT) if end_date else None,
            "period": 86400
        }
        data = self._client.request(path, parameters=params)
        return Queue(data)
