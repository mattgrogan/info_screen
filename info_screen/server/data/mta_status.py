from __future__ import absolute_import

import requests
import xml.etree.ElementTree as ET

from server.data.throttle_mixin import Throttle_Mixin

UPDATE_FREQUENCY = 60 * 10  # Every ten minutes
SERVICE_STATUS_URL = "http://web.mta.info/status/serviceStatus.txt"


class MTA_Status(Throttle_Mixin):
    """
    This class handles connections to mta.info for the current service status.
    """

    def __init__(self):

        self.url = SERVICE_STATUS_URL

        self.service_status = {}   # Dict to hold data

        # Use the Mixin to throttle requests
        self.every(UPDATE_FREQUENCY, self._fetch_data)

    def __getitem__(self, name):
        """
        Checks for new data and returns the appropriate value.
        """

        # Call mixin
        self.run_pending()

        if name in self.service_status.keys():
            return self.service_status[name]
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
                if child.tag == "LIRR":
                    for grandchild in child:
                        line = grandchild.find("name").text
                        status = grandchild.find("status").text
                        self.service_status[line] = status
            return True
        else:
            return False


if __name__ == "__main__":

    cc = MTA_Status()

    print cc["Port Jefferson"]

    for key in cc.service_status.keys():
        print "%s:   %s" % (key, cc[key])
