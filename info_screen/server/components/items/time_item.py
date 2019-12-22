import time

from server.components.layers.text_layer import TextLayer
from util.font_factory import FontFactory

class TimeItem(TextLayer):
    def __init__(self):
        self.font = FontFactory().by_name( "OpenSans-Regular", 160)
        self.color = "#FFFFFF"
        self.callback = lambda: time.strftime("%I:%M", time.localtime()).lstrip("0")
        super(TimeItem, self).__init__(self.font, self.color, self.callback)