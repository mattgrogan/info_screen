import time

from server.components.layers.text_layer import TextLayer
from util.font_factory import FontFactory

class DateItem(TextLayer):
    def __init__(self):
        self.font = FontFactory().by_name( "OpenSans-Regular", 48)
        self.color = "#FFFFFF"
        self.callback = lambda: time.strftime("%A, %B ") + time.strftime("%d").lstrip("0")
        super(DateItem, self).__init__(self.font, self.color, self.callback)