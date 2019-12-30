""" Show NOAA Forecast """
from PIL import ImageDraw

from server.components.layers.screen_layer import ScreenLayer
from server.components.layers.text_layer import TextLayer

from util.font_factory import FontFactory
from server.data.forecast import NOAA_Forecast_Adapter

class Forecast(ScreenLayer):
    """ Show the forecast """

    def __init__(self):
        self.forecast = NOAA_Forecast_Adapter(40.7127837, -73.41639)
        self.pos = ()
        self.orig_pos = ()

        super(Forecast, self).__init__()

        lblfont = FontFactory().by_name("OpenSans-Regular", 16)
        font = FontFactory().by_name("OpenSans-Regular", 14)
        color = "#FFFFFF"

        self.labels = []
        self.weathers = []
        self.temps = []

        for i in range(5):

            self.labels.append(TextLayer(lblfont, "#000000", 
                lambda i=i: self.forecast[i][u"startPeriodName"].upper()))

            self.weathers.append(TextLayer(font, color, 
                lambda i=i: self.forecast[i][u"weather"]))

            self.temps.append(TextLayer(font, color, 
                lambda i=i: self.forecast[i][u"tempLabel"] + " " + self.forecast[i][u"temperature"]))

    def enter(self):

        for label in self.labels:
            label.enter()

        for weather in self.weathers:
            weather.enter() 

        for temp in self.temps:
            temp.enter()

    def step(self):
        for label in self.labels:
            label.step()

        for weather in self.weathers:
            weather.step() 

        for temp in self.temps:
            temp.step()

    def render(self, bg):
        # Save the original position
        if not self.orig_pos:
            self.orig_pos = self.pos

        row_offset = 60
        row_height = 20
        indent = 10

        for i in range(len(self.labels)):
    
            row = i * row_offset

            x, y = self.orig_pos

            # Draw a background
            draw = ImageDraw.Draw(bg)
            draw.rectangle([x - 10, y + row - 4, 800, y + row + row_height - 5], fill="#63a4ff")

            self.labels[i].pos = (x, y + row)
            self.labels[i].render(bg)

            x, y = self.orig_pos

            self.weathers[i].pos = (x + indent, y + row + row_height)
            self.weathers[i].render(bg)

            x, y = self.orig_pos

            self.temps[i].pos = (x + indent, y + row + row_height * 2)
            self.temps[i].render(bg)
