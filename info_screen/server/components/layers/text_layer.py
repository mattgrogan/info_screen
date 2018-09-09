from PIL import Image
import pygame, pygame.font

from util.font_factory import FontFactory
from server.components.layers.screen_layer import ScreenLayer

class TextLayer(ScreenLayer):

    def __init__(self, text, font_name, font_size, color="#FFFFFF"):
        self.text = text
        self.color = color

        pygame.font.init()

        self.font = FontFactory().by_name(font_name, font_size)
    def enter(self):
        pass

    def exit(self):
        pass

    def suspend(self):
        pass

    def resume(self):
        pass

    def step(self):
        pass

    def render(self):

        text = self.font.render(self.text, False, pygame.Color(self.color))

        cropped_text = text.subsurface(text.get_bounding_rect())
  
        # Convert to PIL image for display
        img_str = pygame.image.tostring(cropped_text, "RGBA")
        im = Image.frombytes("RGBA", cropped_text.get_size(), img_str)

        return im