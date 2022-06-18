import logging
from typing import Optional, Union

import anypoint.vendor.mureq as requests

REQUEST_TIMEOUT = 60


class HttpClient:

    def __init__(self, log: logging.Logger):
        self._log = log

    def request(self, url: str,
                method: str = "GET",
                body: Optional[dict] = None,
                headers: Optional[dict] = None,
                parameters: Optional[dict] = None,
                return_json = True
                ) -> Union[dict, requests.Response]:
        try:
            r = requests.request(method,
                                 url,
                                 json=body,
                                 params=parameters,
                                 headers=headers,
                                 timeout=REQUEST_TIMEOUT,
                                 verify=False)
            self._log.debug(f"Received response {method} {url} {parameters if parameters else ''}: {r}")
            if r.status_code >= 400:
                error_message = f"Received a bad response: {method} {url}: {r}: {r.content}"
                raise Exception(error_message)
            return r.json() if return_json else r
        except Exception as e:
            self._log.exception(f"Could not make request {method} {url}: {repr(e)}")
            raise e
