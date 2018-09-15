from __future__ import absolute_import

import requests
import random
import time

from server.data.throttle_mixin import Throttle_Mixin

UPDATE_FREQUENCY = 60 * 120 # Every 120 minutes

class ShowerThoughts(Throttle_Mixin):
    """ This class connects to the showerthoughts subreddit """

    def __init__(self):
        self.url = "https://www.reddit.com/r/Showerthoughts/hot.json"
        self.every(UPDATE_FREQUENCY, self._fetch_data)
        self.data = []

    def _fetch_data(self):
        r = requests.get(self.url, headers = {'User-agent': 'hello reddit'})

        print r.status_code

        if r.status_code == requests.codes.ok:
            self.data = []
            for c in r.json()[u'data'][u'children']:
                self.data.append(c[u'data'][u'title'])

            # Remove the top item
            self.data.pop(0)

    def random(self):

        self.run_pending()

        if len(self.data) == 0:
            self._fetch_data()
            if len(self.data) == 0:
                return ""
        
        i = random.randrange(len(self.data))
        item = self.data[i]
        self.data.pop(i)
        return item
        

if __name__ == "__main__":

    st = ShowerThoughts()

    for i in range(100):
        print st.random().encode('unicode-escape')
        time.sleep(0.5)

