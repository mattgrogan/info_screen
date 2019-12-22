from PIL import Image
import pygame

from server.components.layers.screen_layer import ScreenLayer

class TextLayer(ScreenLayer):

    def __init__(self, font, color, callback):
        super(TextLayer, self).__init__()
        self.font = font
        self.color = color
        self.callback = callback

        self.text = ()
        self.needs_render = False
        self.im = None
        self.rect = None
        self.pos = (0, 0)

    def enter(self):
        self.text = self.callback()
        self.needs_render = True

    def exit(self):
        pass

    def suspend(self):
        pass

    def resume(self):
        pass

    def step(self):
        next_text = self.callback()

        if self.text != next_text:
            self.text = next_text
            self.needs_render = True

    def render(self, bg):
        
        if self.needs_render:
            text, _ = self.font.render(self.text, pygame.Color(self.color))
        
            # Convert to PIL image for display
            img_str = pygame.image.tostring(text, "RGBA")
            im = Image.frombytes("RGBA", text.get_size(), img_str)

            self.im = im
            self.rect = text.get_rect()
            self.needs_render = False

        x = self.rect.x + self.pos[0]
        y = self.rect.y + self.pos[1]

        bg.paste(self.im, box=(x, y), mask=self.im)

        return bg

