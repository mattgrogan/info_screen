""" Allow the user to reset """

from server.components.layers.text_layer import TextLayer
from util.font_factory import FontFactory

class ResetItem(TextLayer):
    """ Allow user to reset the raspberry pi """
    def __init__(self):
        self.font = FontFactory().by_name("OpenSans-Regular", 16)
        self.color = "#FFFFFF"
        self.callback = lambda: "RESET"
        super(ResetItem, self).__init__(self.font, self.color, self.callback)

