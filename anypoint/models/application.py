from datetime import datetime
from typing import Generator, List, TYPE_CHECKING

from anypoint.models.statistics import DashboardStatistics, Statistic
from anypoint.models.worker import Worker, WorkerStatistic

if TYPE_CHECKING:
    from anypoint.api.application import ApplicationApi


class Application:
    def __init__(self, raw_json, client: "ApplicationApi"):
        self.domain: str = raw_json.get("domain")
        self.full_domain: str = raw_json.get("fullDomain")
        self.id: str = raw_json.get("id")
        self.mule_version: str = raw_json.get("muleVersion")
        self.region: str = raw_json.get("region")
        self.status: str = raw_json.get("status")
        self.filename: str = raw_json.get("filename")
        self.deployment_group_id: str = raw_json.get("deploymentGroupId")

        self.num_workers: int = raw_json.get("workers")
        self.remaining_workers: int = raw_json.get("remainingWorkerCount", 0)
        self.environment_id: str = raw_json.get("environment_id")
        self.statistics = None
        self.worker_statistics: List[WorkerStatistic] = []
        self.workers: List[Worker] = []
        self.worker_type = raw_json.get("workerType")
        self.worker_count = raw_json.get("workers", 0)
        self.file_name = raw_json.get("filename")
        self.href = raw_json.get("href")

        self._data = raw_json
        self._api_client = client

        try:
            self.last_update_time: datetime = datetime.utcfromtimestamp(raw_json.get("lastUpdateTime") / 1000)
        except Exception:
            self.last_update_time: datetime = datetime.now()

    def __repr__(self):
        return f"Application({self.full_domain})"

    def __lt__(self, other):
        return self.domain < other.domain

    def get_statistics(self, date_from: datetime, date_to: datetime) -> Generator[Statistic, None, None]:
        return self._api_client.get_application_statistics(self.environment_id, self.domain, date_from, date_to)

    def get_dashboard_statistics(self, date_from: datetime, date_to: datetime) -> DashboardStatistics:
        return self._api_client.get_dashboard_statistics(self.environment_id,
                                                         self.domain,
                                                         date_from,
                                                         date_to)

    def get_status(self):
        return self._api_client.get_application_status(self.environment_id, self.domain)

    def get_insights(self):
        return self._api_client.get_insights(self.environment_id, self.domain)
