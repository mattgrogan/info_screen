"""Show time in HH:MI format"""
import time

from server.components.layers.text_layer import TextLayer
from util.font_factory import FontFactory

class TimeItem(TextLayer):
    """Show time in HH:MI format"""
    def __init__(self):
        self.font = FontFactory().by_name("OpenSans-Regular", 160)
        self.color = "#FFFFFF"
        self.callback = lambda: time.strftime("%I:%M", time.localtime()).lstrip("0")

        self.am_pm = AmpmItem()
        super(TimeItem, self).__init__(self.font, self.color, self.callback)

    def enter(self):
        self.am_pm.enter()
        super(TimeItem, self).enter()

    def step(self):
        self.am_pm.step()
        super(TimeItem, self).step()

    def render(self, bg):
        # First render self
        super(TimeItem, self).render(bg)
        self.am_pm.pos = (self.rect.right + 10, self.rect.top)
        self.am_pm.render(bg)

class AmpmItem(TextLayer):
    """Show AM or PM"""
    def __init__(self):
        self.font = FontFactory().by_name( "OpenSans-Regular", 48)
        self.color = "#FFFFFF"
        self.callback = lambda: time.strftime("%p", time.localtime())
        super(AmpmItem, self).__init__(self.font, self.color, self.callback)