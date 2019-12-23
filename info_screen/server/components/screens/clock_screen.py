""" Main screen showing clock view """

import os
from PIL import Image

from server.components.screens.screen import Screen

from server.components.items.date_item import DateItem
from server.components.items.time_item import TimeItem
from server.components.items.lirr_item import LirrItem
from server.components.items.temp_item import TempItem
from server.components.items.title_item import TitleBar
from server.components.items.reset_item import ResetItem
from server.components.items.sunrise import SunriseItem
from server.components.items.sunset import SunsetItem

class ClockScreen(Screen):
    """ Main screen with clock view"""

    def __init__(self, device):
        self.init()
        self.is_popup = False
        self.device = device

        self._items = []

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
        self.lirr_item.pos = (5, 430)
        self.add_item(self.lirr_item)

        self.temp_item = TempItem()
        self.temp_item.pos = (700, 20)
        self.add_item(self.temp_item)

        self.reset_item = ResetItem()
        self.reset_item.pos = (750, 460)
        self.add_item(self.reset_item)

        self.sunrise_item = SunriseItem()
        self.sunrise_item.pos = (400, 430)
        self.add_item(self.sunrise_item)

        self.sunset_item = SunsetItem()
        self.sunset_item.pos = (550, 430)
        self.add_item(self.sunset_item)

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

    def render(self):

        # Create a blank background
        bg = Image.new("RGBA", self.device.size, "#121212")

        for item in self._items:
            item.render(bg)

        return bg

    def handle_input(self, cmd):
        print "SCREEN: " + cmd

        cmd2 = cmd.split(";")

        if cmd2[0] == "TOUCH":
            x = int(cmd2[1])
            y = int(cmd2[2])

            print "Touch at %i, %i" % (x, y)

            if self.reset_item.rect.collidepoint(x, y):
                print "YOU CLICKED RESTART"
                os.system("sudo reboot")

