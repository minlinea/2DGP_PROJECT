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
image_size = 40

window_top, window_right = 600, 800


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
tile_type = {empty_space : 0, block : 1, thorn : 2}


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
            stickman.y_axiscount = 0
        pass

    @staticmethod
    def exit(stickman, event):
        pass

    @staticmethod
    def do(stickman):
        stickman.frame = (stickman.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        stickman.xpos += stickman.xspeed * game_framework.frame_time
        stickman.xpos = clamp(0 + stickman_size//2, stickman.xpos, window_right - stickman_size//2)

    @staticmethod
    def draw(stickman):
        stickman.image.clip_draw(int(stickman.frame * image_size), stickman.direction * 0, stickman_size, stickman_size * 2 - 1, stickman.xpos,
                                  stickman.ypos)
        pass


class Air:

    @staticmethod
    def enter(stickman, event):
        if event == JUMP:
            stickman.y_axiscount = 1
        elif event == RIGHT_DOWN:
            stickman.xspeed += RUN_SPEED_PPS
            stickman.direction = 1
        elif event == LEFT_DOWN:
            stickman.xspeed -= RUN_SPEED_PPS
            stickman.direction = left
        elif event == RIGHT_UP:
            if (stickman.xspeed != 0):
                stickman.xspeed -= RUN_SPEED_PPS
            stickman.direction = 1
        elif event == LEFT_UP:
            if (stickman.xspeed != 0):
                stickman.xspeed += RUN_SPEED_PPS
            stickman.direction = left
        elif event == INSTANT_DOWN:
            stickman.y_axiscount = 176
            if(stickman.xspeed > 0):
                stickman.direction = right
            else:
                stickman.direction = left
        pass

    @staticmethod
    def exit(stickman, event):
        pass

    @staticmethod
    def do(stickman):
        stickman.frame = (stickman.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        if(stickman.y_axiscount % 6 == 1):
            stickman.yspeed = -((stickman.y_axiscount)//6) + 15
            stickman.y_axiscount += 1
        else:
            stickman.yspeed = 0
            stickman.y_axiscount = (stickman.y_axiscount + 1) % 183

        if(stickman.y_axiscount == 0):
            stickman.y_axiscount = 176

        stickman.ypos += stickman.yspeed #* game_framework.frame_time

        stickman.xpos += stickman.xspeed * game_framework.frame_time
        stickman.xpos = clamp(0 + stickman_size//2, stickman.xpos, window_right - stickman_size//2)
        stickman.ypos = clamp(0 + stickman_size, stickman.ypos, window_top - stickman_size)
        pass

    @staticmethod
    def draw(stickman):
        stickman.image.clip_draw(int(stickman.frame * image_size), stickman.direction * 0,stickman_size, stickman_size * 2 - 1, stickman.xpos,
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
        if (stickman.opacify > 0):
            stickman.opacify -= game_framework.frame_time / 3.0
        else:
            stickman.opacify = 0
        pass

    @staticmethod
    def draw(stickman):
        stickman.image.opacify(stickman.opacify)
        stickman.image.clip_draw(int(stickman.frame * image_size), stickman.direction * 0, stickman_size, stickman_size * 2 - 1, stickman.xpos,
                                  stickman.ypos)
        pass




next_state_table = {
    Ground: {RIGHT_DOWN: Ground, LEFT_UP: Ground, RIGHT_UP: Ground, LEFT_DOWN: Ground, JUMP: Air, INSTANT_DOWN: Ground, LANDING : Ground, DIE : Death},
    Air: {RIGHT_DOWN: Air, RIGHT_UP: Air, LEFT_UP: Air, LEFT_DOWN: Air, JUMP: Air, INSTANT_DOWN: Air, LANDING : Ground, DIE : Death},
    Death: {LEFT_DOWN: Death, RIGHT_DOWN: Death, LEFT_UP: Death, RIGHT_UP: Death, JUMP: Death, INSTANT_DOWN: Death, DIE : Death}
}




class Stickman:
    def __init__(self):
        self.xpos, self.ypos = 150, 280
        self.frame = 0
        self.image = load_image('resource\\character\\animation_sheet_demo.png')
        self.direction = right
        self.xspeed, self.yspeed = 0, 0
        self.y_axiscount = 0
        self.opacify = 1.0
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


    def crash_tile(self, tile_type):
        if (tile_type == block):
            if(self.xspeed > 0):
                self.xpos = (self.xpos // 40) * 40 + 20
                self.xspeed = 0
            elif (self.xspeed < 0):
                self.xpos = (self.xpos // 40) * 40 + 20
                self.xspeed = 0
            elif (self.y_axiscount >= 93):
                self.y_axiscount = 0
                self.ypos = (self.ypos // 40 + 1 ) * 40
                self.add_event(LANDING)
            elif (self.y_axiscount < 93):
                self.y_axiscount = 180 - self.y_axiscount
                self.ypos = (self.ypos // 40) * 40
        elif (tile_type == empty_space):
            pass
        elif (tile_type > 3):
            self.add_event(DIE)

    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_bb())


    def get_bb(self):
        return self.xpos - stickman_size//2, self.ypos - stickman_size, self.xpos + stickman_size//2, self.ypos+stickman_size

    def add_event(self, event):
        self.event_que.insert(0, event)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)