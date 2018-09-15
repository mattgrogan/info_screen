from __future__ import absolute_import

import os
import requests
import xml.etree.ElementTree as ET

from server.data.throttle_mixin import Throttle_Mixin

UPDATE_FREQUENCY = 60 * 10 # Every ten minutes

class NOAA_Current_Observation(Throttle_Mixin):
  """
  This class handles connections to weather.gov for the current observation.
  """

  def __init__(self, station):

    self.station = station
    self.url = "http://w1.weather.gov/xml/current_obs/%s.xml" % station

    self.current_obs = {}   # Dict to hold observation data

    # Use the Mixin to throttle requests
    self.every(UPDATE_FREQUENCY, self._fetch_data)

  def __getitem__(self, name):
    """
    Checks for new data and returns the appropriate value.
    """

    # Call mixin
    self.run_pending()

    if name in self.current_obs.keys():
      return self.current_obs[name]
    else:
      raise ValueError("No value for '%s'" % name)

  def _fetch_data(self):

    # Attempt a connection
    try:
      r = requests.get(self.url, timeout=10)
    except:
      return False

    if r.status_code == requests.codes.ok:
      # Parse the data
      try:
        root = ET.fromstring(r.content)
      except:
        return False
        
      for child in root:
        self.current_obs[child.tag] = child.text
      return True
    else:
      return False

class IconDecoder(object):
      
  def __init__(self):
    self.icons = {
      # Mostly cloudy
      "bkn": u"\uF002",
      "nbkn": u"\uF086",
      # Fair
      "skc": u"\uF00D",
      "nskc": u"\uF02E",
      # A few clouds
      "few": u"\uF002",
      "nfew": u"\uF086",
      # Partly cloudy
      "sct": u"\uF002",
      "nsct": u"\uF086",
      # Overcast
      "ovc": u"\uF013",
      "novc": u"\uF013",
      # Fog
      "fg": u"\uF0B6",
      "nfg": u"\uF04A",
      # Smoke
      "smoke": u"\uF062",
      # Freezing rain
      "fzra": u"\uF0B5",
      # Ice pellets
      "ip": u"\uF01B",
      # Freezing rain snow
      "mix": u"\uF006",
      "nmix": u"\uF026",
      # Rain ice pellets
      "raip": u"\uF027",
      # Rain Snow
      "rasn": u"\uF0B2",
      "nrasn": u"\uF0B4",
      # Rain showers
      "shra": u"\uF01A",
      # Thunderstorm
      "tsra": u"\uF010",
      "ntsra": u"\uF02D",
      # Snow
      "sn": u"\uF00A",
      "nsn": u"\uF038",
      # Wind
      "wind": u"\uF085",
      "nwind": u"\uF023",
      # Showers in vicinity
      "hi_shwrs": u"\uF01A",
      "hi_nshwrs": u"\uF01A",
      # Freezing rain rain
      "fzrara": u"\uF0B5",
      # Tstorm in vicinity
      "hi_tsra": u"\uF010",
      "hi_ntsra": u"\uF02D",
      # Light rain
      "ra1": u"\uF00B",
      "nra": u"\uF02B",
      # Rain
      "ra": u"\uF04E",
      # "nra":
      # Funnel cloud
      "nsvrtsra": u"\uF056",
      # Dust
      "dust": u"\uF063",
      # Haze
      "mist": u"\uF014"
    }
  
  def lookup(self, icon_url_name):
    base, ext = os.path.splitext(icon_url_name)
    return self.icons[base]

if __name__ == "__main__":

  cc = NOAA_Current_Observation("KLGA")

  print cc["temp_f"]

  print cc.current_obs.keys()

  for key in cc.current_obs.keys():
    print "%s:   %s" % (key, cc[key])
  
  print cc["temp_f"]
  print cc["observation_time"]

  icon = IconDecoder()
  print cc["icon_url_name"]
  print icon.lookup(cc["icon_url_name"]).encode('unicode-escape')
