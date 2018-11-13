import game_framework
import threading

from pico2d import *
from enum import Enum

state = Enum('state', 'ground, air, hold, death, waiting')


class Tile:
    image = None
    size = 40

    def __init__(self, vertical, horizon, state):
        self.y, self.x = vertical, horizon
        self.type = 0
        if(state == 'run'):
            if(self.image == None):
               self.image = load_image('resource\\tile\\stage_run_tile_kind.png')
        elif (state == 'return'):
            if (self.image == None):
                self.image = load_image('resource\\tile\\stage_return_tile_kind.png')
        elif (state == 'editor'):
            if (self.image == None):
                self.image = load_image('resource\\tile\\tile_kind.png')



    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(1 + 2 * (self.type % 2) + (40 * (self.type % 2)), 1,
                                self.size, self.size, 20 + self.x * self.size, 20 + self.y * self.size)
        #self.image.clip_draw(1 + (40 * (self.type % 2)), 1 + ((40 * 4) - (40 * ((self.type + 2) // 2))),
                            #self.size, self.size, 20 + self.x * self.size, 20 + self.y * self.size)

        #draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x * self.size + 1, self.y * self.size + 1, (self.x + 1) * self.size - 1, (self.y + 1) * self.size - 1
