""" Show current sunrise status """
from PIL import ImageDraw

from server.components.layers.text_layer import TextLayer
from util.font_factory import FontFactory
from server.data.sunrise_sunset import Sunrise_Sunset


class SunsetItem(TextLayer):
    """ Show the current sunrise time """

    def __init__(self):
        # Data services
        self.sun = Sunrise_Sunset(40.7127837,  -74.0059413)
        self.orig_pos = ()

        self.sunset = Sunset(self.sun)

        self.font = FontFactory().by_name("OpenSans-Regular", 18)
        self.color = "#FFFFFF"
        self.callback = lambda: "Sunset"
        super(SunsetItem, self).__init__(self.font, self.color, self.callback)

    def enter(self):
        self.sunset.enter()
        super(SunsetItem, self).enter()

    def step(self):
        self.sunset.step()
        super(SunsetItem, self).step()

    def render(self, bg):
        # Save the original position
        if not self.orig_pos:
            self.orig_pos = self.pos

        # Draw a box
        draw = ImageDraw.Draw(bg)
        x, y = self.orig_pos
        w = 5
        h = 40
        draw.rectangle([self.orig_pos, (x + w, y + h)], fill="#6200ea")

        # Move position to the right and draw the label
        self.pos = (x + w + 5, y)
        super(SunsetItem, self).render(bg)

        # Move the position down and draw the status
        self.sunset.pos = (x + w + 5, self.rect.bottom + 5)
        self.sunset.render(bg)

class Sunset(TextLayer):
    """ Show the current status """
    def __init__(self, sun):
        self.sun = sun

        self.font = FontFactory().by_name("OpenSans-Regular", 24)
        self.color = "#FFFFFF"
        self.callback = self.status
        super(Sunset, self).__init__(self.font, self.color, self.callback)

    def status(self):
        """ Return the status to be displayed on screen """
        try:
            s = self.sun["sunset"].strftime("%I:%M %p").lstrip("0")
        except ValueError:
            return "NA"
        
        return s





