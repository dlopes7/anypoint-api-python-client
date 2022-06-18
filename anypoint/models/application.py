from datetime import datetime
from typing import Generator, List, TYPE_CHECKING

from anypoint.models.statistics import DashboardStatistics, Statistic
from anypoint.models.worker import Worker, WorkerStatistic

if TYPE_CHECKING:
    from anypoint import Anypoint


class Application:
    def __init__(self, raw_json, client: "Anypoint"):
        self.domain: str = raw_json["domain"]
        self.full_domain: str = raw_json["fullDomain"]
        self.id: str = raw_json["id"]
        self.mule_version: str = raw_json["muleVersion"]
        self.region: str = raw_json["region"]
        self.status: str = raw_json["status"]
        self.filename: str = raw_json["filename"]
        self.deployment_group_id: str = raw_json["deploymentGroupId"]

        self.num_workers: int = raw_json["workers"]
        self.remaining_workers: int = raw_json["remainingWorkerCount"]
        self.environment_id: str = raw_json["environment_id"]
        self.statistics = None
        self.worker_statistics: List[WorkerStatistic] = []
        self.workers: List[Worker] = []

        self._data = raw_json
        self._api_client = client

        try:
            self.last_update_time: datetime = datetime.utcfromtimestamp(raw_json["lastUpdateTime"] / 1000)
        except Exception:
            self.last_update_time: datetime = datetime.now()

    def __repr__(self):
        return f"Application({self.full_domain})"

    def __lt__(self, other):
        return self.domain < other.domain

    def get_statistics(self, date_from: datetime, date_to: datetime) -> Generator[Statistic, None, None]:
        return self._api_client.get_application_statistics(self.environment_id, self.domain, date_from, date_to)

    def get_dashboard_statistics(self, date_from: datetime, date_to: datetime) -> DashboardStatistics:
        return self._api_client.get_application_dashboard_statistics(self.environment_id,
                                                                     self.domain,
                                                                     date_from,
                                                                     date_to)
