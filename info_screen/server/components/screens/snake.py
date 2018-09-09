import random
import time

from collections import deque
from PIL import Image, ImageColor

from server.components.screens.screen import Screen
from util.timedelta import TimeDelta

class SnakeScreen(Screen):

    def __init__(self, device):
        
        self.device = device
        self.width, self.height = device.size

        self.direction = "RIGHT"
        self.snakehead = None
        self.apple = (None, None)
        self.segments = deque()
        self.segment_count = None
        self.max_segment_count = 1024
        self.movespeed = 150.0

        self.is_setup = False
        self.is_popup = False
        self.timedelta = TimeDelta().reset()

        self.snake_color = ImageColor.getrgb("#FFFDB7")
        self.apple_color = ImageColor.getrgb("#1BA363")
        self.black_color = (0, 0, 0)

    def new_apple(self):
        
        while True:
            # Find a random place for the apple
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            # Check that there's no overlap
            if not (x, y) in self.segments:
                self.apple = (x, y)
                break

    def handle_input(self, cmd):
        
        if cmd == "KEY_UP":
            if self.direction != "DOWN":
                self.direction = "UP"
        elif cmd == "KEY_DOWN":
            if self.direction != "UP":
                self.direction = "DOWN"
        elif cmd == "KEY_LEFT":
            if self.direction != "RIGHT":
                self.direction = "LEFT"
        elif cmd == "KEY_RIGHT":
            if self.direction != "LEFT":
                self.direction = "RIGHT"

    def update(self):
        
        x, y = self.snakehead

        if self.direction == "UP":
            y -= 1
        elif self.direction == "DOWN":
            y += 1
        elif self.direction == "LEFT":
            x -= 1
        elif self.direction == "RIGHT":
            x += 1

        # Wrap around X axis
        if x >= self.width:
            x = 0
        elif x < 0:
            x = self.width - 1

        # Wrap around Y axis
        if y >= self.height:
            y = 0
        elif y < 0:
            y = self.height - 1

        # Has the snake hit itself?
        if (x, y) in self.segments:
            self.die()

        # Add the point to the queue
        self.segments.appendleft((x, y))

        # Check if we hit the apple
        if (x, y) == self.apple:
            self.segment_count += 1

            if self.segment_count > self.max_segment_count:
                self.segment_count = self.max_segment_count

            self.new_apple()

        # Trim the end of the snake
        while (len(self.segments) > self.segment_count):
            p = self.segments.pop()

        self.snakehead = (x, y)

    def die(self):
        time.sleep(1)
        self.setup()

    def setup(self):
        self.new_apple()
        self.snakehead = (self.width / 2, self.height / 2)
        self.direction = "RIGHT"
        self.segments = deque()
        self.segment_count = 4

        self.timedelta = TimeDelta().reset()

        self.is_setup = True

    def enter(self):
        self.setup()

    def exit(self):
        raise NotImplementedError

    def suspend(self):
        raise NotImplementedError

    def resume(self):
        raise NotImplementedError

    def step(self):
        if self.timedelta.test(self.movespeed / 1000.0):
            self.update()
            self.timedelta.reset()

    def render(self):
        
        if not self.is_setup:
            self.setup()
            
        # Create a blank background
        bg = Image.new("RGBA", self.device.size)
        pix = bg.load()

        pix[self.apple] = self.apple_color
        for point in list(self.segments):
            pix[point] = self.snake_color

        return bg




        

