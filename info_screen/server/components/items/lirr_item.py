""" Show current LIRR status """

from server.components.layers.text_layer import TextLayer
from util.font_factory import FontFactory
from server.data.mta_status import MTA_Status


class LirrItem(TextLayer):
    """ Show the current LIRR status """

    def __init__(self):
        # Data services
        self.service_status = MTA_Status()
        self.line = "Port Jefferson"

        self.font = FontFactory().by_name("OpenSans-Regular", 24)
        self.color = "#FFFFFF"
        self.callback = self.status
        super(LirrItem, self).__init__(self.font, self.color, self.callback)

    def status(self):
        """ Return status to be displayed on screen """
        try:
            s = self.line + ": " + self.service_status[self.line]
        except ValueError:
            return "NA"

        return s




