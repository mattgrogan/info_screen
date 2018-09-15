import time
from PIL import Image

from util.font_factory import FontFactory

from server.components.screens.screen import Screen
from server.components.layers.text_layer import TextLayer
from server.components.layers.scrolling_layer import ScrollingLayer
from server.components.screens.gif_screen_factory import GifScreenFactory

from server.data.current_conditions import NOAA_Current_Observation, IconDecoder

STATION = "KFRG"

class ClockScreen(Screen):

    def __init__(self, device):
        self.init()
        self.is_popup = False
        self.device = device

        # Create a connection to the NOAA website 
        self.current_obs = NOAA_Current_Observation(STATION)

        # Load the font
        self.vl_font = FontFactory().by_name( "enhanced_led_board-7", 80)
        self.lg_font = FontFactory().by_name( "enhanced_led_board-7", 48)
        self.md_font = FontFactory().by_name( "enhanced_led_board-7", 32)
        self.sm_font = FontFactory().by_name( "enhanced_led_board-7", 24)
        self.vs_font = FontFactory().by_name( "enhanced_led_board-7", 16)

        self.lg_icons = FontFactory().by_name( "weathericons-regular-webfont", 32)
        self.md_icons = FontFactory().by_name( "weathericons-regular-webfont", 24)
        self.sm_icons = FontFactory().by_name( "weathericons-regular-webfont", 16)

        # Create colors
        self.green = "#a1d99b"
        self.red = "#fc9272"
        self.blue = "#9ecae1"

        self.time_color = self.green
        self.outside_color = self.blue

        # Time and Date

        self.time_text = TextLayer(self.vl_font, self.time_color, lambda: time.strftime("%I:%M", time.localtime()).lstrip("0"))
        self.time_text.padding = (10, 10, 0, 0)

        self.am_pm = TextLayer(self.md_font, self.time_color, lambda: time.strftime("%p", time.localtime()))
        self.am_pm.padding = (10, 10, 0, 0)
        self.am_pm.left_items = [self.time_text]

        self.date_text = TextLayer(self.vs_font, self.time_color, lambda: time.strftime("%A %B ") + time.strftime("%d").lstrip("0"))
        self.date_text.padding = (10, 5, 0, 0)
        self.date_text.top_items = [self.time_text]

        # Outside conditions

        self.weather_icon = TextLayer(self.lg_icons, self.outside_color, self._weather_icon)
        self.weather_icon.padding = (10, 10, 0, 0)
        self.weather_icon.top_items = [self.time_text, self.date_text]

        self.temp = TextLayer(self.md_font, self.outside_color, self._temp)
        self.temp.padding = (10, 10, 0, 0)
        self.temp.top_items = [self.time_text, self.date_text]
        self.temp.left_items = [self.weather_icon]

        self.temp_icon = TextLayer(self.md_icons, self.outside_color, lambda: u"\uF045")
        self.temp_icon.padding = (5, 10, 0, 0)
        self.temp_icon.top_items = [self.time_text, self.date_text]
        self.temp_icon.left_items = [self.weather_icon, self.temp]

        self.rh = TextLayer(self.md_font, self.outside_color, self._rh)
        self.rh.padding = (10, 10, 0, 0)
        self.rh.top_items =[self.time_text, self.date_text]
        self.rh.left_items = [self.weather_icon, self.temp, self.temp_icon]

        self.rh_icon = TextLayer(self.sm_icons, self.outside_color, lambda: u"\uF07A")
        self.rh_icon.padding = (5, 10, 0, 0)
        self.rh_icon.top_items = [self.time_text, self.date_text]
        self.rh_icon.left_items = [self.weather_icon, self.temp, self.temp_icon, self.rh]

        # Weather text

        self.weather = TextLayer(self.vs_font, self.outside_color, self._weather)
        self.weather.padding = (10, 5, 0, 0)
        self.weather.top_items = [self.time_text, self.date_text, self.weather_icon]

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

        self.weather_icon.step()
        self.temp.step()
        self.temp_icon.step()
        self.rh.step()
        self.rh_icon.step()
        self.weather.step()

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

    def render(self):
        
        # Create a blank background
        bg = Image.new("RGBA", self.device.size, "#000000")

        self.time_text.render(bg)
        self.am_pm.render(bg)
        self.date_text.render(bg)

        self.weather_icon.render(bg)
        self.temp.render(bg)
        self.temp_icon.render(bg)
        self.rh.render(bg)
        self.rh_icon.render(bg)
        self.weather.render(bg)

        return bg

    def handle_input(self, cmd):
        pass
    
