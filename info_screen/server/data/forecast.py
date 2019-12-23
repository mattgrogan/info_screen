from __future__ import absolute_import

import requests
import json

from server.data.throttle_mixin import Throttle_Mixin


class NOAA_Forecast(Throttle_Mixin):
    """ Obtain a forecast from weather.gov """

    def __init__(self, lat, lon, timeout=2):
        """
        lat, lon: coordinates of the forecast
        """

        self.timeout = timeout

        self.url = "https://forecast.weather.gov/MapClick.php?lat=40.73443&lon=-73.41639&FcstType=json"

        self._results = {}

        self.every(60 * 60, self._fetch_data)

    def __getitem__(self, key):
        """ Retrieve an item, if it doesn't exist, return an empty set """

        # Call Mixin
        self.run_pending()

        if key in self._results.keys():
            data = self._results[key]
        else:
            data = ""

        return data

    def _fetch_data(self):

        try:
            r = requests.get(self.url, timeout=self.timeout)
        except:
            return False

        if r.status_code == requests.codes.ok:
            self._results = json.loads(r.content)
            return True
        else:
            self._results = {}
            return False


class NOAA_Forecast_Adapter(object):
    """
    Adapter to make it easier to get forecast data
    """

    def __init__(self, lat, lon, timeout=2):
        self._noaa_forecast = NOAA_Forecast(lat, lon, timeout)

    def __getitem__(self, key):

        result = {}

        time_fields = ["startPeriodName", "startValidTime", "tempLabel"]
        data_fields = ["temperature", "weather", "iconLink", "text"]

        for field in time_fields:
            result[field] = self._noaa_forecast["time"][field][key]

        for field in data_fields:
            result[field] = self._noaa_forecast["data"][field][key]

        return result


if __name__ == "__main__":
    f = NOAA_Forecast_Adapter(40.7127837, -73.41639)

    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(f[0])
