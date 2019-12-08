import time
from PIL import Image

from util.font_factory import FontFactory

from server.components.screens.screen import Screen
from server.components.layers.text_layer import TextLayer
from server.components.layers.scrolling_layer import ScrollingLayer
from server.components.screens.gif_screen_factory import GifScreenFactory

from server.data.current_conditions import NOAA_Current_Observation, IconDecoder
from server.data.mta_status import MTA_Status

STATION = "KFRG"
ST_INTERVAL = 60 * 10 # every 10 minutes

class ClockScreen(Screen):

    def __init__(self, device):
        self.init()
        self.is_popup = False
        self.device = device

        # Create a connection to the NOAA website 
        self.current_obs = NOAA_Current_Observation(STATION)

        # Create a connection to MTA
        self.service_status = MTA_Status()
        self.line = "Port Jefferson"

        # Load the font
        self.el_font = FontFactory().by_name( "OpenSans-Regular", 160)
        self.vl_font = FontFactory().by_name( "OpenSans-Regular", 120)
        self.lg_font = FontFactory().by_name( "OpenSans-Regular", 80)
        self.md_font = FontFactory().by_name( "OpenSans-Regular", 48)
        self.sm_font = FontFactory().by_name( "OpenSans-Regular", 24)
        self.vs_font = FontFactory().by_name( "OpenSans-Regular", 16)
        self.ty_font = FontFactory().by_name( "OpenSans-Regular", 8)

        self.lg_icons = FontFactory().by_name( "weathericons-regular-webfont", 120)
        self.md_icons = FontFactory().by_name( "weathericons-regular-webfont", 32)
        self.sm_icons = FontFactory().by_name( "weathericons-regular-webfont", 24)

        # Create colors
        self.green = "#a1d99b"
        self.red = "#fc9272"
        self.blue = "#9ecae1"

        self.time_color = self.green
        self.outside_color = self.blue
        self.st_color = self.red

        # Time and Date

        self.date_text = TextLayer(self.md_font, self.time_color, lambda: time.strftime("%A, %B ") + time.strftime("%d").lstrip("0"))
        self.date_text.padding = (10, 5, 0, 0)
        
        self.time_text = TextLayer(self.el_font, self.time_color, lambda: time.strftime("%I:%M", time.localtime()).lstrip("0"))
        self.time_text.padding = (10, 10, 0, 0)
        self.time_text.top_items = [self.date_text]

        self.am_pm = TextLayer(self.md_font, self.time_color, lambda: time.strftime("%p", time.localtime()))
        self.am_pm.padding = (10, 10, 0, 0)
        self.am_pm.top_items = [self.date_text]

        self.am_pm.left_items = [self.time_text]


        # Outside conditions

        self.outside_conditions = TextLayer(self.sm_font, self.outside_color, lambda: "Current Conditions")
        self.outside_conditions.padding = (10, 20, 0, 0)
        self.outside_conditions.top_items = [self.time_text, self.date_text]

        self.weather_icon = TextLayer(self.lg_icons, self.outside_color, self._weather_icon)
        self.weather_icon.padding = (10, 10, 0, 0)
        self.weather_icon.top_items = [self.time_text, self.date_text, self.outside_conditions]

        self.temp = TextLayer(self.md_font, self.outside_color, self._temp)
        self.temp.padding = (10, 15, 0, 0)
        self.temp.top_items = [self.time_text, self.date_text, self.outside_conditions]
        self.temp.left_items = [self.weather_icon]

        self.temp_icon = TextLayer(self.md_icons, self.outside_color, lambda: u"\uF045")
        self.temp_icon.padding = (5, 15, 0, 0)
        self.temp_icon.top_items = [self.time_text, self.date_text, self.outside_conditions]
        self.temp_icon.left_items = [self.weather_icon, self.temp]

        self.rh = TextLayer(self.md_font, self.outside_color, self._rh)
        self.rh.padding = (10, 15, 0, 0)
        self.rh.top_items =[self.time_text, self.date_text, self.outside_conditions, self.temp]
        self.rh.left_items = [self.weather_icon]

        self.rh_icon = TextLayer(self.sm_icons, self.outside_color, lambda: u"\uF07A")
        self.rh_icon.padding = (5, 15, 0, 0)
        self.rh_icon.top_items = [self.time_text, self.date_text, self.outside_conditions, self.temp]
        self.rh_icon.left_items = [self.weather_icon, self.rh]

        # Weather text

        self.weather = TextLayer(self.sm_font, self.outside_color, self._weather)
        self.weather.padding = (10, 5, 0, 0)
        self.weather.top_items = [self.time_text, self.date_text, self.outside_conditions, self.weather_icon]

        # MTA Status
        self.port_jeff = TextLayer(self.sm_font, "#0039a6", self._service_status)
        self.port_jeff.padding = (5, 15, 0, 0)
        self.port_jeff.top_items = [self.time_text, self.date_text, self.outside_conditions, self.weather_icon, self.weather]

        # Restart
        self.restart = TextLayer(self.vs_font, "#FF0000", lambda: "RESTART")
        self.restart.padding = (5, 5, 5, 5)
        self.restart.top_items = [self.time_text, self.date_text, self.outside_conditions, self.weather_icon, self.weather, self.port_jeff]

    def enter(self):
        pass

    def exit(self):
        pass

    def suspend(self):
        pass

    def resume(self):
        pass

    def step(self):
        self.time_text.step()
        self.am_pm.step()
        self.date_text.step()

        self.outside_conditions.step()
        self.weather_icon.step()
        self.temp.step()
        self.temp_icon.step()
        self.rh.step()
        self.rh_icon.step()
        self.weather.step()
        self.port_jeff.step()
        self.restart.step()

    def _temp(self):
        try:
            temp_str = "%i" % int(float(self.current_obs["temp_f"]))
        except ValueError:
            temp_str = "NA"

        return temp_str

    def _rh(self):
        try:
            rh_str = "%i" % int(float(self.current_obs["relative_humidity"]))
        except ValueError:
            rh_str = "NA"

        return rh_str

    def _weather(self):
        try:
            w_str = self.current_obs["weather"]
        except ValueError:
            w_str = "NA"

        return w_str  

    def _weather_icon(self):
        try:
            w_str = self.current_obs['icon_url_name']
        except ValueError:
            return ""

        icon = IconDecoder()

        return icon.lookup(w_str)

    def _service_status(self):
        try:
            s_str = self.line + ": " + self.service_status[self.line]
        except ValueError:
            return "NA"

        return s_str          

    def render(self):
        
        # Create a blank background
        bg = Image.new("RGBA", self.device.size, "#000000")

        self.time_text.render(bg)
        self.am_pm.render(bg)
        self.date_text.render(bg)

        self.outside_conditions.render(bg)
        self.weather_icon.render(bg)
        self.temp.render(bg)
        self.temp_icon.render(bg)
        self.rh.render(bg)
        self.rh_icon.render(bg)
        self.weather.render(bg)
        self.port_jeff.render(bg)
        self.restart.render(bg)

        return bg

    def handle_input(self, cmd):
        print "SCREEN: " + cmd

        cmd2 = cmd.split(";")

        if cmd2[0] == "TOUCH":
            x = int(cmd2[1])
            y = int(cmd2[2])

            print "Touch at %i, %i" % (x, y)

            if self.port_jeff.rect.collidepoint(x, y):
                print "YOU CLICKED PORT JEFF"
            if self.restart.rect.collidepoint(x, y):
                print "YOU CLICKED RESTART"
   
