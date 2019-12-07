from __future__ import absolute_import

import time
import pygame
from pygame.locals import *

from messaging.command_connection import CommandConnection
from messaging.image_connection import ImageConnection

MATRIX_WIDTH = 800
MATRIX_HEIGHT = 480

CMD_HOST = "localhost"
CMD_PORT = 5555

IMG_HOST = "localhost"
IMG_PORT = 5556

FPS = 30

class Rpi(object):

    def __init__(self):
        # Connect to receive images
        self.image_conn = ImageConnection()
        self.image_conn.connect(IMG_HOST, IMG_PORT, as_receiver=True)

        pygame.init()
        self._display_surf = pygame.display.set_mode((MATRIX_WIDTH, MATRIX_HEIGHT))
        pygame.display.set_caption("Info Screen")

        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()

        self.running = True

    def mainloop(self):

        while self.running:
            self.clock.tick(FPS)

            for event in pygame.event.get():        # gets all the events which have occured till now and keeps tab of them.
                ## listening for the the X button at the top
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                else:
                    print event

            im = self.image_conn.receive()
            if im is not None:
                self.display(im)

    def display(self, im):
        
        raw_str = im.tobytes()
        s = pygame.image.fromstring(raw_str, (MATRIX_WIDTH, MATRIX_HEIGHT), 'RGB')

        
        self._display_surf.blit(s, (0, 0))
        pygame.display.flip()
            

            
        


