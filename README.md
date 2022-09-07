# Anypoint python client

```python
import logging
from datetime import datetime, timedelta

from anypoint import Anypoint


def main():
    client = Anypoint("user", "password")
    org = client.get_organization()
    print(org.name, org.id)

    for environment in org.get_environments():
        for app in environment.get_applications():
            statistics = app.get_dashboard_statistics(datetime.utcnow() - timedelta(minutes=5), datetime.utcnow())
            for event in statistics.events:
                print(event.timestamp, event.value)
            for worker in statistics.workers:
                for metric in worker.metrics:
                    print(metric.metric_id, metric.metrics)


if __name__ == '__main__':
    main()


```
