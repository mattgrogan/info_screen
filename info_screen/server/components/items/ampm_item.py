import time

from server.components.layers.text_layer import TextLayer
from util.font_factory import FontFactory

class AmpmItem(TextLayer):
    def __init__(self):
        self.font = FontFactory().by_name( "OpenSans-Regular", 48)
        self.color = "#FFFFFF"
        self.callback = lambda: time.strftime("%p", time.localtime())
        super(AmpmItem, self).__init__(self.font, self.color, self.callback)