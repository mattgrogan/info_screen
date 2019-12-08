from PIL import Image
import pygame

from server.components.layers.screen_layer import ScreenLayer

class TextLayer(ScreenLayer):

    def __init__(self, font, color, callback, padding=(0, 0, 0, 0)):
        # padding is left, top, right, bottom
        self.font = font
        self.color = color
        self.callback = callback
        self.padding = padding

        self.text = ()
        self.left_items = [] # Which items appear left of this item
        self.top_items = []  # Which items appear above this item
        self.needs_render = False
        self.im = None
        self.rect = None

    @property
    def size(self):
        if self.im is None:
            w = 0
            h = 0
        else:
            w, h = self.im.size

        left, top, right, bottom = self.padding
        return (left + w + right, top + h + bottom)

    @property
    def x(self):
        left, top, right, bottom = self.padding
        return left

    @property
    def y(self):
        left, top, right, bottom = self.padding
        return top

    @property
    def w(self):
        w, h = self.size
        return w
    
    @property
    def h(self):
        w, h = self.size
        return h

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
            text, r = self.font.render(self.text, pygame.Color(self.color))
        
            # Convert to PIL image for display
            img_str = pygame.image.tostring(text, "RGBA")
            im = Image.frombytes("RGBA", text.get_size(), img_str)

            self.im = im
            self.needs_render = False

        x = self.x
        y = self.y

        for item in self.left_items:
            x += item.w

        for item in self.top_items:
            y += item.h

        self.rect = pygame.Rect(x, y, self.w, self.h)

        bg.paste(self.im, box=(x, y), mask=self.im)

        return bg

