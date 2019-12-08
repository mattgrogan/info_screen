from __future__ import absolute_import
from __future__ import print_function

from builtins import object
import time
import pygame
from pygame.locals import *
import ft5406

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

        # Set up connection to send commands
        self.cmd = CommandConnection()
        self.cmd.connect(CMD_HOST, CMD_PORT, as_receiver=False)

        pygame.init()
        self._display_surf = pygame.display.set_mode((MATRIX_WIDTH, MATRIX_HEIGHT))
        pygame.display.set_caption("Info Screen")

        #pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()

        self.ts = ft5406.Touchscreen()
        self.touch_id = -1

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

            for touch in self.ts.poll():
                if touch.valid:
                    if self.touch_id != touch.id: # we ignore multiple coords for the same touch event
                        self.cmd.send_touch(touch.x, touch.y)
                        self.touch_id = touch.id
                        print(touch.slot, touch.id, touch.valid, touch.x, touch.y)
                        pygame.draw.circle(self._display_surf, (0, 0, 255), (touch.x, touch.y), 5)
                        pygame.display.update()

                # elif event.type == pygame.MOUSEBUTTONDOWN:
                #     pos = event.pos
                #     print("DETECTED AT %i, %i" % pos)
                #     pygame.draw.circle(self._display_surf, (0, 0, 255), pos, 5)
                #     pygame.display.update()
                # elif event.type == pygame.MOUSEBUTTONUP:
                #     pos = event.pos
                #     print("DETECTED AT %i, %i" % pos)
                #     pygame.draw.circle(self._display_surf, (0, 255, 0), pos, 5)
                #     pygame.display.update()
                # else:
                #     print(event)

            im = self.image_conn.receive()
            if im is not None:
                # self.display(im)
                pass

    def display(self, im):
        
        raw_str = im.tobytes()
        s = pygame.image.fromstring(raw_str, (MATRIX_WIDTH, MATRIX_HEIGHT), 'RGB')

        
        self._display_surf.blit(s, (0, 0))
        pygame.display.flip()
            

            
        


