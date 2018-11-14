import game_framework

from pico2d import *


class Image:
    def __init__(self, x, y, left, bottom, width, height, title):
        self.x, self.y = x,y
        self.left, self.bottom = left, bottom
        self.width, self.height =  width, height
        self.image = load_image(title)


    def draw(self):
        self.image.clip_draw(self.left,self.bottom,self.width, self.height,self.x,self.y)
