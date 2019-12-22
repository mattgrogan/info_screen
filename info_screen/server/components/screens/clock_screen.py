""" Main screen showing clock view """

from PIL import Image

from server.components.screens.screen import Screen

from server.components.items.date_item import DateItem
from server.components.items.time_item import TimeItem
from server.components.items.lirr_item import LirrItem
from server.components.items.temp_item import TempItem
from server.components.items.title_item import TitleBar

# from server.data.current_conditions import NOAA_Current_Observation, IconDecoder

# STATION = "KFRG"
# ST_INTERVAL = 60 * 10 # every 10 minutes


class ClockScreen(Screen):
    """ Main screen with clock view"""

    def __init__(self, device):
        self.init()
        self.is_popup = False
        self.device = device

        self._items = []
        # # Create a connection to the NOAA website
        # self.current_obs = NOAA_Current_Observation(STATION)

        # Load the font
        # self.el_font = FontFactory().by_name( "OpenSans-Regular", 160)
        # self.vl_font = FontFactory().by_name( "OpenSans-Regular", 120)
        # self.lg_font = FontFactory().by_name( "OpenSans-Regular", 80)
        # self.md_font = FontFactory().by_name( "OpenSans-Regular", 48)
        # self.sm_font = FontFactory().by_name( "OpenSans-Regular", 24)
        # self.vs_font = FontFactory().by_name( "OpenSans-Regular", 16)
        # self.ty_font = FontFactory().by_name( "OpenSans-Regular", 8)

        # self.lg_icons = FontFactory().by_name( "weathericons-regular-webfont", 120)
        # self.md_icons = FontFactory().by_name( "weathericons-regular-webfont", 32)
        # self.sm_icons = FontFactory().by_name( "weathericons-regular-webfont", 24)

        # Create colors
        # self.green = "#a1d99b"
        # self.red = "#fc9272"
        # self.blue = "#9ecae1"

        # self.time_color = self.green
        # self.outside_color = self.blue
        # self.st_color = self.red

        # Time and Date
        self.title_bar = TitleBar()
        self.title_bar.pos = [0, 0, 800, 70]
        self.add_item(self.title_bar)

        self.date_text = DateItem()
        self.date_text.pos = (20, 15)
        self.add_item(self.date_text)

        self.time_text = TimeItem()
        self.time_text.pos = (20, 100)
        self.add_item(self.time_text)

        self.lirr_item = LirrItem()
        self.lirr_item.pos = (20, 450)
        self.add_item(self.lirr_item)

        self.temp_item = TempItem()
        self.temp_item.pos = (700, 20)
        self.add_item(self.temp_item)







        # Weather

        # self.weather_icon = TextLayer(self.lg_icons, self.outside_color, self._weather_icon)
        # self.weather_icon.padding = (10, 10, 0, 0)
        # self.weather_icon.top_items = [self.time_text, self.date_text]

        # self.temp = TextLayer(self.md_font, self.outside_color, self._temp)
        # self.temp.padding = (10, 15, 0, 0)
        # self.temp.top_items = [self.time_text, self.date_text]
        # self.temp.left_items = [self.weather_icon]

        # self.temp_icon = TextLayer(self.md_icons, self.outside_color, lambda: u"\uF045")
        # self.temp_icon.padding = (5, 15, 0, 0)
        # self.temp_icon.top_items = [self.time_text, self.date_text]
        # self.temp_icon.left_items = [self.weather_icon, self.temp]

        # self.rh = TextLayer(self.md_font, self.outside_color, self._rh)
        # self.rh.padding = (10, 15, 0, 0)
        # self.rh.top_items =[self.time_text, self.date_text, self.temp]
        # self.rh.left_items = [self.weather_icon]

        # self.rh_icon = TextLayer(self.sm_icons, self.outside_color, lambda: u"\uF07A")
        # self.rh_icon.padding = (5, 15, 0, 0)
        # self.rh_icon.top_items = [self.time_text, self.date_text, self.temp]
        # self.rh_icon.left_items = [self.weather_icon, self.rh]

        # Weather text

        # self.weather = TextLayer(self.sm_font, self.outside_color, self._weather)
        # self.weather.padding = (10, 5, 0, 0)
        # self.weather.top_items = [self.time_text, self.date_text, self.weather_icon]

        # Restart
        # self.restart = TextLayer(self.vs_font, "#FF0000", lambda: "RESTART")
        # self.restart.padding = (10, 10, 10, 10)
        # self.restart.top_items = [self.time_text, self.date_text,
        #   self.weather_icon, self.weather, self.port_jeff]

    def add_item(self, item):
        """ Add an item to the list of items """
        self._items.append(item)

    def enter(self):
        pass

    def exit(self):
        pass

    def suspend(self):
        pass

    def resume(self):
        pass

    def step(self):

        for item in self._items:
            item.step()

        # self.weather_icon.step()
        # self.temp.step()
        # self.temp_icon.step()
        # self.rh.step()
        # self.rh_icon.step()
        # self.weather.step()
        # self.port_jeff.step()
        # self.restart.step()

    # def _temp(self):
    #     try:
    #         temp_str = "%i" % int(float(self.current_obs["temp_f"]))
    #     except ValueError:
    #         temp_str = "NA"

    #     return temp_str

    # def _rh(self):
    #     try:
    #         rh_str = "%i" % int(float(self.current_obs["relative_humidity"]))
    #     except ValueError:
    #         rh_str = "NA"

    #     return rh_str

    # def _weather(self):
    #     try:
    #         w_str = self.current_obs["weather"]
    #     except ValueError:
    #         w_str = "NA"

    #     return w_str

    # def _weather_icon(self):
    #     try:
    #         w_str = self.current_obs['icon_url_name']
    #     except ValueError:
    #         return ""

    #     icon = IconDecoder()

    #     return icon.lookup(w_str)


    def render(self):

        # Create a blank background
        bg = Image.new("RGBA", self.device.size, "#121212")

        for item in self._items:
            item.render(bg)

        # self.weather_icon.render(bg)
        # self.temp.render(bg)
        # self.temp_icon.render(bg)
        # self.rh.render(bg)
        # self.rh_icon.render(bg)
        # self.weather.render(bg)
        # self.restart.render(bg)

        return bg

    def handle_input(self, cmd):
        print "SCREEN: " + cmd

        cmd2 = cmd.split(";")

        if cmd2[0] == "TOUCH":
            x = int(cmd2[1])
            y = int(cmd2[2])

            print "Touch at %i, %i" % (x, y)

            for item in self._items:
                if item.rect.collidepoint(x, y):
                    print type(item)

            # if self.port_jeff.rect.collidepoint(x, y):
            #     print "YOU CLICKED PORT JEFF"
            # if self.restart.rect.collidepoint(x, y):
            #     print "YOU CLICKED RESTART"
            #     os.system("sudo reboot")

