# Anypoint python client

```python

from datetime import datetime, timedelta

from anypoint import Anypoint
from anypoint.authentication import  OAuth2


def main():
    auth = OAuth2("connected_app_client_id", "connected_app_client_secret")
    client = Anypoint(auth)
    org = client.organizations.get_organization()
    print(org.name, org.id)

    for environment in org.get_environments():
        for app in environment.get_applications():
            statistics = app.get_dashboard_statistics(datetime.utcnow() - timedelta(minutes=5), datetime.utcnow())
            for event in statistics.events:
                print(event.timestamp, event.value)
            for worker in statistics.workers:
                for metric in worker.metrics:
                    print(metric.metric_id, metric.statistics)


if __name__ == '__main__':
    main()


```
