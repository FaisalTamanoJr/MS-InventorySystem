from dateutil import tz
import math


# Convert date to local timezone and in a more accessible format
def convert_to_local_datetime(date, format="%d %B %Y"):
    if date:
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        utc = date
        utc = utc.replace(tzinfo=from_zone)
        desired_date_format = utc.astimezone(to_zone)
        desired_date_format = desired_date_format.strftime(format)
        return desired_date_format
    return "N/A"


# Trims a given number without rounding it off
def truncate(f, n):
    return math.floor(f * 10 ** n) / 10 ** n

def isfloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False