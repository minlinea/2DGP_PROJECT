import game_framework
import tile

from pico2d import *


# Boy Run Speed
# fill expressions correctly
PIXEL_PER_METER = (10.0 / 0.3) # 10pixel 30cm
RUN_SPEED_KMPH = 20.0 #km / hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
# fill expressions correctly
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4


stickman_size = 39
tile_size = 40

window_top, window_right = 600, 800

jump_momentum = RUN_SPEED_KMPH * 20
jump_momentum_reduction = 3

stickman = None




# stickman Event
RIGHT_DOWN, RIGHT_UP, LEFT_DOWN, LEFT_UP, JUMP, INSTANT_DOWN, LANDING, DIE = range(8)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_UP): JUMP,
    (SDL_KEYDOWN, SDLK_DOWN): INSTANT_DOWN,
}

left, right = range(2)
direction = {left : 0, right : 1}
empty_space, block, thorn = range(3)
tile_type = {empty_space : 0, block : 1, thorn : 4}


#state

class Ground:
    @staticmethod
    def enter(stickman, event):
        if event == RIGHT_DOWN:
            stickman.xspeed += RUN_SPEED_PPS
            stickman.direction =right
        elif event == LEFT_DOWN:
            stickman.xspeed -=  RUN_SPEED_PPS
            stickman.direction = left
        elif event == RIGHT_UP:
            if (stickman.xspeed != 0):
                stickman.xspeed -= RUN_SPEED_PPS
            stickman.direction = right
        elif event == LEFT_UP:
            if (stickman.xspeed != 0):
                stickman.xspeed += RUN_SPEED_PPS
            stickman.direction = left
        elif event == LANDING:
            pass
        stickman.yspeed = 0
        stickman.crash = False
        pass

    @staticmethod
    def exit(stickman, event):
        pass

    @staticmethod
    def do(stickman):
        stickman.frame = (stickman.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        if not (stickman.crash):
            stickman.xpos += stickman.xspeed * game_framework.frame_time
        stickman.xpos = clamp(0 + stickman_size//2, stickman.xpos, window_right - stickman_size//2)

    @staticmethod
    def draw(stickman):
        stickman.image.clip_draw(int(stickman.frame * tile_size), stickman.direction, stickman_size, stickman_size * 2 - 1, stickman.xpos,
                                  stickman.ypos)
        pass


class Air:

    @staticmethod
    def enter(stickman, event):
        if event == JUMP:
            if(stickman.yspeed == 0):
                stickman.yspeed = jump_momentum
        elif event == RIGHT_DOWN:
            stickman.xspeed += RUN_SPEED_PPS
            stickman.direction = right
        elif event == LEFT_DOWN:
            stickman.xspeed -= RUN_SPEED_PPS
            stickman.direction = left
        elif event == RIGHT_UP:
            if (stickman.xspeed != 0):
                stickman.xspeed -= RUN_SPEED_PPS
            stickman.direction = right
        elif event == LEFT_UP:
            if (stickman.xspeed != 0):
                stickman.xspeed += RUN_SPEED_PPS
            stickman.direction = left
        elif event == INSTANT_DOWN:
            stickman.yspeed = 0
        stickman.crash = False
        pass

    @staticmethod
    def exit(stickman, event):
        if(event == LANDING):
            stickman.ypos = (stickman.ypos // tile_size + 1) * tile_size
            stickman.yspeed = 0
        pass

    @staticmethod
    def do(stickman):
        stickman.frame = (stickman.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

        stickman.calculation_yspeed()
        stickman.ypos += stickman.yspeed * game_framework.frame_time

        if not (stickman.crash):
            stickman.xpos += stickman.xspeed * game_framework.frame_time
        stickman.xpos = clamp(0 + stickman_size//2, stickman.xpos, window_right - stickman_size//2)
        stickman.ypos = clamp(0 + stickman_size, stickman.ypos, window_top - stickman_size)
        pass

    @staticmethod
    def draw(stickman):
        stickman.image.clip_draw(int(stickman.frame * tile_size), stickman.direction * 0,stickman_size, stickman_size * 2 - 1, stickman.xpos,
                                  stickman.ypos)
        pass


class Death:
    def enter(stickman, event):
        stickman.xspeed = 0
        stickman.yspeed = 0
        pass

    @staticmethod
    def exit(stickman, event):
        pass

    @staticmethod
    def do(stickman):
        stickman.opacify_variation = game_framework.frame_time / 3.0
        if (stickman.opacify > 0):
            stickman.opacify -= stickman.opacify_variation
        else:
            stickman.opacify = 0
        pass

    @staticmethod
    def draw(stickman):
        stickman.image.opacify(stickman.opacify)
        stickman.image.clip_draw(int(stickman.frame * tile_size), stickman.direction * 0, stickman_size, stickman_size * 2 - 1, stickman.xpos,
                                  stickman.ypos)
        pass




next_state_table = {
    Ground: {RIGHT_DOWN: Ground, LEFT_UP: Ground, RIGHT_UP: Ground, LEFT_DOWN: Ground, JUMP: Air, INSTANT_DOWN: Ground, LANDING : Ground, DIE : Death},
    Air: {RIGHT_DOWN: Air, RIGHT_UP: Air, LEFT_UP: Air, LEFT_DOWN: Air, JUMP: Air, INSTANT_DOWN: Air, LANDING : Ground, DIE : Death},
    Death: {LEFT_DOWN: Death, RIGHT_DOWN: Death, LEFT_UP: Death, RIGHT_UP: Death, JUMP: Death, INSTANT_DOWN: Death, DIE : Death}
}




class Stickman:
    def __init__(self):
        self.xpos, self.ypos = 150, 280+1
        self.frame = 0
        self.image = load_image('resource\\character\\animation_sheet_demo.png')
        self.direction = right
        self.xspeed, self.yspeed = 0, 0
        self.opacify = 1.0
        self.opacify_variation = 1.0
        self.crash = False
        self.event_que = []
        self.cur_state = Ground
        self.cur_state.enter(self, None)


    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)


    def calculation_yspeed(self):
        self.yspeed = self.yspeed - jump_momentum_reduction

        if(self.yspeed <= -jump_momentum and self.cur_state == Air):
            self.yspeed = -jump_momentum



    def crash_tile(self, tile_type, j, i):
        stickman_x, stickman_y = self.xpos // 40, self.ypos // 40
        if (tile_type >= thorn):
            self.add_event(DIE)
        elif (tile_type == block):
            if ((i == stickman_x + 1 or i == stickman_x - 1) and (j == stickman_y or j == stickman_y-1)):
                self.xpos = (self.xpos // 40) * 40 + 20
                self.crash = True
            elif (j== stickman_y + 1 and i == stickman_x) and self.yspeed >0:
                self.yspeed = -self.yspeed
                self.ypos = (self.ypos // 40) * 40 + 1
            elif ((j== stickman_y - 1 and i == stickman_x) and self.yspeed <=0):
                self.add_event(LANDING)




    def draw(self):
        self.cur_state.draw(self)

    def get_bb(self):
        return self.xpos - stickman_size//2, self.ypos - stickman_size, self.xpos + stickman_size//2, self.ypos+stickman_size

    def add_event(self, event):
        self.event_que.insert(0, event)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)