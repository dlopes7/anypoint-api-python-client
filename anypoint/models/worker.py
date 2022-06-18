from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from anypoint import Anypoint


class Worker:
    def __init__(self, raw_json, client: "Anypoint"):
        self.id = raw_json["id"]
        self.host = raw_json["host"]
        self.port = raw_json["port"]
        self.status = raw_json["status"]
        self.deployed_region = raw_json["deployedRegion"]

        self._data = raw_json
        self._api_client = client

    def __repr__(self):
        return f"Worker({self.id})"


class WorkerStatistic:
    def __init__(self, raw_json, client: "Anypoint"):
        self.id = raw_json["id"]
        self.disk_read_bytes = self.get_latest_value("diskReadBytes")
        self.disk_write_bytes = self.get_latest_value("diskWriteBytes")
        self.network_in = self.get_latest_value("networkIn")
        self.network_out = self.get_latest_value("networkOut")
        self.memory_total_used = self.get_latest_value("memoryTotalUsed")
        self.memory_percent_used = self.get_latest_value("memoryPercentageUsed")
        self.cpu = self.get_latest_value("cpu")
        self.memory_total_max = raw_json["statistics"]["memoryTotalMax"] if "memoryTotalMax" in raw_json[
            "statistics"] else -1

        self._data = raw_json
        self._api_client = client

    def get_latest_value(self, metric_name) -> float:
        if metric_name in self._data["statistics"] and self._data["statistics"][metric_name]:
            return list(self._data["statistics"][metric_name].values())[-1]
        return -1

    def __repr__(self):
        return f"Worker {self.id} CPU: {self.cpu}%, MEM: {self.memory_percent_used:.2f}%"
