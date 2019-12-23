import pygame, pygame.freetype

class FontFactory(object):

    def __init__(self):
        pygame.freetype.init()


    def from_file(self, filename, size):

        pygame.freetype.init()
        font = pygame.freetype.Font(filename, size)

        return font

    def by_size(self, size):

        if size == "SMALL":
            font = self.from_file("fonts/visitor1.ttf", 10)

        elif size == "MEDIUM":
            font = self.from_file("fonts/small_pixel.ttf", 8)

        elif size == "HUGE":
            font = self.from_file("fonts/m12.ttf", 32)

        elif size == "FALCON":
            font = self.from_file("fonts/Falcon Patrol.ttf", 7)

        elif size == "SMALLEST":
            font = self.from_file("fonts/smallest_pixel-7.ttf", 10)

        else:
            font = self.from_file("fonts/smallest_pixel-7.ttf", size)

        return font

    def by_name(self, name, size):
        font = pygame.freetype.Font("fonts/" + name + ".ttf", size)
        return font



