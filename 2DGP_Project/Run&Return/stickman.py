import game_framework
import tile

from pico2d import *
from music import Effect

# Boy Run Speed
# fill expressions correctly
PIXEL_PER_METER = (10.0 / 0.3) # 10pixel 30cm
RUN_SPEED_KMPH = 30.0 #km / hour
JUMP_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
# fill expressions correctly
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 7
tile_size = 40

window_top, window_right = 600, 800

jump_momentum = JUMP_SPEED_KMPH * 20
jump_momentum_reduction = 3

stickman = None




# stickman Event
RIGHT_DOWN, RIGHT_UP, LEFT_DOWN, LEFT_UP, JUMP, INSTANT_DOWN, LANDING, FALL, DIE = range(9)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_UP): JUMP,
    (SDL_KEYDOWN, SDLK_DOWN): INSTANT_DOWN,
}

right, left  = range(2)
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
        stickman.x_crash = False

    @staticmethod
    def exit(stickman, event):
        if (event == LANDING):
            stickman.ypos = (stickman.ypos // tile_size + 1) * tile_size
            stickman.yspeed = 0

    @staticmethod
    def do(stickman):
        stickman.frame = (stickman.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

        stickman.calculation_yspeed()
        stickman.ypos += stickman.yspeed * game_framework.frame_time

        if not (stickman.x_crash):
            stickman.xspeed = clamp(-RUN_SPEED_PPS, stickman.xspeed, RUN_SPEED_PPS)
            stickman.xpos += stickman.xspeed * game_framework.frame_time
            stickman.run_distance += abs(stickman.xspeed * game_framework.frame_time)
        stickman.xpos = clamp(0 + stickman.size//2, stickman.xpos, window_right - stickman.size//2)


    @staticmethod
    def draw(stickman):
        stickman.image.clip_draw(int(stickman.frame) * 100, stickman.direction * stickman.size * 2 + stickman.direction, stickman.size, stickman.size * 2, stickman.xpos,
                                  stickman.ypos)


class Air:

    @staticmethod
    def enter(stickman, event):
        if event == JUMP:
            if not (stickman.jump_lock):
                stickman.jump_lock = True
                stickman.yspeed = jump_momentum
                stickman.play_jump_sound()
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
            stickman.yspeed = -jump_momentum
        elif event == FALL:
            pass
        stickman.x_crash = False

    @staticmethod
    def exit(stickman, event):
        if(event == LANDING):
            stickman.ypos = (stickman.ypos // tile_size + 1) * tile_size
            stickman.yspeed = 0
            stickman.jump_lock = False

    @staticmethod
    def do(stickman):
        stickman.frame = (stickman.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        stickman.calculation_yspeed()
        stickman.ypos += stickman.yspeed * game_framework.frame_time
        if(stickman.ypos - stickman.size < -stickman.size ):
            stickman.add_event(DIE)
        if not (stickman.x_crash):
            stickman.xspeed = clamp(-RUN_SPEED_PPS, stickman.xspeed, RUN_SPEED_PPS)
            stickman.xpos += stickman.xspeed * game_framework.frame_time
            stickman.run_distance += abs(stickman.xspeed * game_framework.frame_time)
        stickman.xpos = clamp(0 + stickman.size//2, stickman.xpos, window_right - stickman.size//2)


    @staticmethod
    def draw(stickman):
        stickman.image.clip_draw(int(stickman.frame) * 100, stickman.direction * stickman.size * 2 + 1,stickman.size, stickman.size * 2, stickman.xpos,
                                  stickman.ypos)


class Death:

    @staticmethod
    def enter(stickman, event):
        stickman.xspeed = 0
        stickman.yspeed = 0
        #stickman.play_death_sound()

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

    @staticmethod
    def draw(stickman):
        stickman.image.opacify(stickman.opacify)
        stickman.image.clip_draw(int(stickman.frame * tile_size), stickman.direction * stickman.size * 2, stickman.size, stickman.size * 2 - 1, stickman.xpos,
                                  stickman.ypos)




next_state_table = {
    Ground: {RIGHT_DOWN: Ground, LEFT_UP: Ground, RIGHT_UP: Ground, LEFT_DOWN: Ground, JUMP: Air, INSTANT_DOWN: Ground, LANDING : Ground, FALL : Air, DIE : Death},
    Air: {RIGHT_DOWN: Air, RIGHT_UP: Air, LEFT_UP: Air, LEFT_DOWN: Air, JUMP: Air, INSTANT_DOWN: Air, LANDING : Ground, FALL: Air, DIE : Death},
    Death: {LEFT_DOWN: Death, RIGHT_DOWN: Death, LEFT_UP: Death, RIGHT_UP: Death, JUMP: Death, INSTANT_DOWN: Death, LANDING:Death, FALL: Death, DIE : Death}
}




class Stickman:
    def __init__(self):
        self.xpos, self.ypos = 60, 280
        self.frame = 0.8
        self.image = load_image('resource\\character\\stage_run_animation_sheet.png')
        self.direction = right
        self.xspeed, self.yspeed = 0, 0
        self.opacify = 1.0
        self.opacify_variation = 1.0
        self.run_distance = 0.0
        self.size = 40
        self.x_crash = False
        self.jump_lock = False
        self.event_que = []
        self.cur_state = Ground
        self.cur_state.enter(self, None)
        self.jump_sound = Effect('jump')
        #self.death_sound = Effect('death')

    def play_jump_sound(self):
        self.jump_sound.play()

    def play_landing_sound(self):
        self.landing_sound.play()

    def play_death_sound(self):
        self.death_sound.play()

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
        elif (self.cur_state == Ground and self.yspeed <=-jump_momentum_reduction):
            self.add_event(FALL)



    def crash_tile(self, tile_type, j, i):
        stickman_x, stickman_y = self.xpos // tile_size, self.ypos // tile_size

        if (tile_type >= thorn):
            self.add_event(DIE)
        elif (tile_type == block):
            if (i == stickman_x + 1 and (j == stickman_y or j == stickman_y-1)):
                stickman_x_interval = self.xpos - (stickman_x)* tile_size-1
                self.xpos = (stickman_x) * tile_size + stickman_x_interval
                self.x_crash = True
            elif (i == stickman_x - 1 and (j == stickman_y or j == stickman_y-1)):
                stickman_x_interval = self.xpos - (stickman_x) * tile_size+1
                self.xpos = (stickman_x) * tile_size + stickman_x_interval
                self.x_crash = True
            elif (j== stickman_y + 1 and i == stickman_x) and self.yspeed >0:
                self.yspeed = -self.yspeed
                self.ypos = (self.ypos // tile_size) * tile_size
            elif ((j== stickman_y - 1 and i == stickman_x) and self.yspeed <=0):
                self.add_event(LANDING)

    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.xpos - self.size//2, self.ypos - self.size, self.xpos + self.size//2, self.ypos+self.size

    def external_add_event(self, event):
        if(event == "DIE"):
            self.add_event(DIE)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)