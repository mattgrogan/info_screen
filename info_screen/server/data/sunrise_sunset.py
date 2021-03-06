"""
Access the https://sunrise-sunset.org API
"""
from __future__ import absolute_import

import requests
import json
import iso8601
from dateutil import tz

from server.data.throttle_mixin import Throttle_Mixin

class Sunrise_Sunset(Throttle_Mixin):

  def __init__(self, lat, lng, date="today", local_time=True, timeout=0.5):
    """
    Initialize the object.
    lat, lng: The coordinates to lookup
    date: date in YYYY-MM-DD format or relative date formats
    localtime: boolean. Convert time values to local time
    timeout: timeout in seconds
    """

    self._opts = {
        "lat": lat,
        "lng": lng,
        "date": date,
        "formatted": 0  # Do not format the dates
    }

    self.local_time = local_time
    self.timeout = timeout
    self.url = "https://api.sunrise-sunset.org/json"
    self._results = {}

    # Use the Mixin to throttle requests
    self.every(60 * 10, self.update)

  def __getitem__(self, key):
    """ Retrieve an item. If it doesn't exist, return an empty string """

    # Call mixin
    self.run_pending()

    if key in self._results.keys():

      dt = self._results[key]

      if self.local_time:
        dt = iso8601.parse_date(dt)
        dt = dt.astimezone(tz.tzlocal())

    else:
      dt = ""

    return dt

  def update(self):
    """
    Retrieve new results from the server
    """

    try:
      r = requests.get(self.url, params=self._opts, timeout=self.timeout)
    except:
      return False

    if r.status_code == requests.codes.ok:
      self._results = json.loads(r.content)["results"]
      return True
    else:
      self._results = {}
      return False


if __name__ == "__main__":
  sun = Sunrise_Sunset(40.7127837,  -74.0059413)
  # sun.update()
  print "Sunrise: " + str(sun["sunrise"])
  print "Sunset: " + str(sun["sunset"])
