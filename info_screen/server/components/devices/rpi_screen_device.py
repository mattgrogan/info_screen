from PIL import Image

from server.components.devices.graphics_device import GraphicsDevice

IMAGE_SIZE = (800, 480)

class RpiScreenDevice(GraphicsDevice):
    """ The graphics device handles image conversion to
        ensure the correct mode and size. """

    def __init__(self):
        self.size = IMAGE_SIZE
