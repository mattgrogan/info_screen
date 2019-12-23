""" Show current LIRR status """
from PIL import ImageDraw

from server.components.layers.text_layer import TextLayer
from util.font_factory import FontFactory
from server.data.mta_status import MTA_Status


class LirrItem(TextLayer):
    """ Show the current LIRR status """

    def __init__(self):
        # Data services
        self.service_status = MTA_Status()
        self.line = "Port Jefferson"
        self.orig_pos = ()

        self.lirr_item_status = LirrItemStatus(self.line, self.service_status)

        self.font = FontFactory().by_name("OpenSans-Regular", 18)
        self.color = "#FFFFFF"
        self.callback = lambda: self.line
        super(LirrItem, self).__init__(self.font, self.color, self.callback)

    def enter(self):
        self.lirr_item_status.enter()
        super(LirrItem, self).enter()

    def step(self):
        self.lirr_item_status.step()
        super(LirrItem, self).step()

    def render(self, bg):
        # Save the original position
        if not self.orig_pos:
            self.orig_pos = self.pos

        # Draw a box
        draw = ImageDraw.Draw(bg)
        x, y = self.orig_pos
        w = 5
        h = 40
        draw.rectangle([self.orig_pos, (x + w, y + h)], fill="#004ba0")

        # Move position to the right and draw the label
        self.pos = (x + w + 5, y)
        super(LirrItem, self).render(bg)

        # Move the position down and draw the status
        self.lirr_item_status.pos = (x + w + 5, self.rect.bottom + 5)
        self.lirr_item_status.render(bg)





class LirrItemStatus(TextLayer):
    """ Show the current status """
    def __init__(self, line, service_status):
        self.line = line
        self.service_status = service_status

        self.font = FontFactory().by_name("OpenSans-Regular", 24)
        self.color = "#FFFFFF"
        self.callback = self.status
        super(LirrItemStatus, self).__init__(self.font, self.color, self.callback)

    def status(self):
        """ Return the status to be displayed on screen """
        try:
            s = self.service_status[self.line]
        except ValueError:
            return "NA"
        
        return s

    def render(self, bg):
        if self.status() == "GOOD SERVICE":
            self.color = "#00c853"
        else:
            self.color = "#dd2c00"

        super(LirrItemStatus, self).render(bg)




