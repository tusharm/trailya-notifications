from datetime import datetime, timezone

from dateutil.parser import parse
from dateutil.tz import gettz


def to_epoch_millis(d: datetime):
    return d.astimezone(timezone.utc).timestamp() * 1000


def as_string(date: datetime):
    return date.strftime('%Y-%m-%d')


def parse_to_utc(src: str, tzstr: str) -> datetime:
    parsed = parse(f'{src} AST', tzinfos={'AST': gettz(tzstr)})
    return parsed.astimezone(timezone.utc)


def now_as_utc() -> datetime:
    return datetime.now().astimezone(timezone.utc)
