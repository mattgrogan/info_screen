""" Show temperature from NOAA """

from server.components.layers.text_layer import TextLayer
from util.font_factory import FontFactory

from server.data.current_conditions import NOAA_Current_Observation, IconDecoder
STATION = "KFRG"
ST_INTERVAL = 60 * 5 # every 5 minutes

class TempItem(TextLayer):
    """ Show the temperature """
    def __init__(self):
        # Create a connection to the NOAA website
        self.current_obs = NOAA_Current_Observation(STATION)

        self.font = FontFactory().by_name("OpenSans-Regular", 48)
        self.color = "#FFFFFF"
        self.callback = self.temp

        self.icon = TempIcon()

        super(TempItem, self).__init__(self.font, self.color, self.callback)

    def enter(self):
        self.icon.enter()
        super(TempItem, self).enter()

    def step(self):
        self.icon.step()
        super(TempItem, self).step()

    def render(self, bg):
        super(TempItem, self).render(bg)
        self.icon.pos = (self.rect.right + 5, self.rect.top)
        self.icon.render(bg)

    def temp(self):
        """ Return the temperature as an integer """
        try:
            s = "%i" % int(float(self.current_obs["temp_f"]))
        except ValueError:
            return "NA"

        return s

class TempIcon(TextLayer):
    """ Show a degrees ()F symbol """
    def __init__(self):
        self.font = FontFactory().by_name( "weathericons-regular-webfont", 32)
        self.color = "#FFFFFF"
        self.callback = lambda: u"\uF045"

        super(TempIcon, self).__init__(self.font, self.color, self.callback)
       