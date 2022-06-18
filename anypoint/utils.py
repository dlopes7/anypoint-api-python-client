from datetime import datetime

from .constants import DATE_FORMAT


def date_to_str(date: datetime) -> str:
    return date.strftime(DATE_FORMAT)
