"""Show trash and recycling icons
"""
import time
from PIL import Image

from server.components.layers.text_layer import TextLayer
from util.font_factory import FontFactory

from server.data.huntington_trash import TrashDay

class TrashItem(TextLayer):

    def __init__(self):
        self.td = TrashDay()

        self.font = FontFactory().by_name("OpenSans-Regular", 18)
        self.color = "#FFFFFF"
        self.callback = self.text

        super(TrashItem, self).__init__(self.font, self.color, self.callback)

    def enter(self):
        super(TrashItem, self).enter()

    def step(self):
        super(TrashItem, self).step()

    def text(self):
        dt = time.strftime("%Y-%m-%d")
        s = " | ".join(self.td[dt])
        return "TODAY: %s" % s
        
    def render(self, bg):
        super(TrashItem, self).render(bg)