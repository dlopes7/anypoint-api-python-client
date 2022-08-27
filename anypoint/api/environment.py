import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from anypoint import Anypoint


class EnvironmentApi:
    def __init__(self, client: "Anypoint", log: logging.Logger):
        self._client = client
        self._log = log
