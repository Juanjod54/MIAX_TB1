import re
import pytz
from datetime import datetime


class Util:
    @staticmethod
    def to_utc(dt: datetime) -> datetime:
        return dt.astimezone(pytz.utc)

    @staticmethod
    def from_str(dt: str, pattern: str, timezone:str=None) -> datetime:
        dt = datetime.strptime(dt, pattern)
        if timezone:
            dt.replace(tzinfo=pytz.timezone(timezone))
        return dt

    @staticmethod
    def datetime_to_MM_DD_YYYY_format(date: datetime) -> str:
        return date.strftime("%m-%d-%Y")

    @staticmethod
    def transform_keys(data: dict, regex: str) -> dict:
        new_data = {}
        if data:
            for key, value in data.items():
                results = re.match(regex, key)
                new_key = results.group(1) if results else key
                new_data[new_key] = Util.transform_keys(value, regex) if isinstance(value, dict) else value

        return new_data