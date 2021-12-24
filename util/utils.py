import pytz as pytz


def get_datetime_as_timezone(dt, tz=pytz.utc):
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=pytz.utc)
    return dt.astimezone(tz)
