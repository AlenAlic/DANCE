from datetime import timezone, datetime
from backend.constants import DATETIME_FORMAT


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


def datetime_python(s):
    return datetime.strptime(s, DATETIME_FORMAT)


def datetime_browser(dt):
    return dt.strftime(DATETIME_FORMAT)


def shift_list(lst, offset=0):
    return lst[-offset % len(lst):] + lst[:-offset % len(lst)]
