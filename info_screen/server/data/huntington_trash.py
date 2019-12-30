"""
Display the trash or recycling icon
"""
from __future__ import absolute_import, print_function
from collections import OrderedDict

import xmltodict

class TrashDay(object):
    """
    This class handles parsing the trash and recycling calendar from huntingtonny.gov
    """

    def __init__(self):

        self._data = {}

        with open('./server/data/huntington_calendar.xml') as fd:
            doc = xmltodict.parse(fd.read())

            events = doc["icalendar"]["vcalendar"]["components"]["vevent"]

            for event in events:
                event_props = event["properties"]
                summary = event_props["summary"]["text"]

                dates = event_props.get("rdate")

                if dates is not None:
                    if isinstance(dates, list):
                        for date in dates:
                            dt = date["date-time"][:10]
                            self[dt] = summary
                    elif isinstance(dates, OrderedDict):
                        dt = dates["date-time"][:10]
                        self[dt] = summary

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, val):
        # Ensure the value is a list
        if key in self._data:
            self._data[key].append(val)
        else:
            self._data[key] = [val]

if __name__ == "__main__":
    print("Huntington NY Trash Dates")
    td = TrashDay()
    print(td["2019-12-30"])

    print(td["2020-01-23"])

