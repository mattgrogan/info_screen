import time
from PIL import Image

from util.font_factory import FontFactory

from server.components.screens.screen import Screen
from server.components.layers.text_layer import TextLayer
from server.components.layers.scrolling_layer import ScrollingLayer
from server.components.screens.gif_screen_factory import GifScreenFactory

from server.data.current_conditions import NOAA_Current_Observation

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

        self.weather_icons = FontFactory().by_name( "weathericons-regular-webfont", 24)

        # Create colors
        self.green = "#a1d99b"
        self.red = "#fc9272"
        self.blue = "#9ecae1"

        self.time_color = self.green
        self.outside_color = self.blue

        self.time_text = TextLayer(self.vl_font, self.time_color, lambda: time.strftime("%I:%M", time.localtime()).lstrip("0"))
        self.time_text.padding = (10, 10, 0, 0)

        self.am_pm = TextLayer(self.md_font, self.time_color, lambda: time.strftime("%p", time.localtime()))
        self.am_pm.padding = (10, 10, 0, 0)
        self.am_pm.left_items = [self.time_text]

        self.date_text = TextLayer(self.vs_font, self.time_color, lambda: time.strftime("%A %B ") + time.strftime("%d").lstrip("0"))
        self.date_text.padding = (10, 5, 0, 0)
        self.date_text.top_items = [self.time_text]

        self.temp = TextLayer(self.md_font, self.outside_color, self._temp)
        self.temp.padding = (10, 10, 0, 0)
        self.temp.top_items = [self.time_text, self.date_text]

        self.temp_icon = TextLayer(self.weather_icons, self.outside_color, lambda: u"\uF045")
        self.temp_icon.padding = (5, 10, 0, 0)
        self.temp_icon.top_items = [self.time_text, self.date_text]
        self.temp_icon.left_items = [self.temp]

        self.rh = TextLayer(self.md_font, self.outside_color, self._rh)
        self.rh.padding = (10, 10, 0, 0)
        self.rh.top_items =[self.time_text, self.date_text]
        self.rh.left_items = [self.temp, self.temp_icon]

        self.rh_icon = TextLayer(self.weather_icons, self.outside_color, lambda: u"\uF07A")
        self.rh_icon.padding = (5, 10, 0, 0)
        self.rh_icon.top_items = [self.time_text, self.date_text]
        self.rh_icon.left_items = [self.temp, self.temp_icon, self.rh]


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
        self.temp.step()
        self.temp_icon.step()
        self.rh.step()
        self.rh_icon.step()

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

    def render(self):
        
        # Create a blank background
        bg = Image.new("RGBA", self.device.size, "#000000")

        self.time_text.render(bg)
        self.am_pm.render(bg)
        self.date_text.render(bg)

        self.temp.render(bg)
        self.temp_icon.render(bg)
        self.rh.render(bg)
        self.rh_icon.render(bg)

        return bg

    def handle_input(self, cmd):
        pass
    
