from datetime import datetime, timezone

from dateutil.parser import parse


def as_string(date: datetime):
    return date.strftime('%Y-%m-%d')


def parse_to_utc(isoformatted_datetime_with_tz: str) -> datetime:
    return parse(isoformatted_datetime_with_tz).astimezone(timezone.utc)


def build_isoformat_string(date: str, time: str):
    # TODO: find the offset dynamically
    tzoffset = "+10:00"

    return f'{date}T{time}{tzoffset}'
