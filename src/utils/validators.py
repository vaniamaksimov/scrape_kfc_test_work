from datetime import datetime, time

from dateparser import parse


def parse_from_string(stringed_datetime: str) -> datetime:
    return parse(stringed_datetime)


def datetime_validator(stringed_datetime: str) -> datetime | None:
    if not stringed_datetime:
        return
    return parse_from_string(stringed_datetime)


def time_validator(stringed_time: str) -> time | None:
    if not stringed_time:
        return
    return parse_from_string(stringed_time).time()
