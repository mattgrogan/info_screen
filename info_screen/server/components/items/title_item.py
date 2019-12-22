""" Draw a title bar """
from PIL import ImageDraw

from server.components.layers.screen_layer import ScreenLayer

class TitleBar(ScreenLayer):
    """ Show a title """

    def __init__(self):
        self.pos = None
        super(TitleBar, self).__init__()

    def step(self):
        pass

    def render(self, bg):
        """ Draw a bar across the top of the screen """

        draw = ImageDraw.Draw(bg)
        draw.rectangle(self.pos, fill="#004ba0")