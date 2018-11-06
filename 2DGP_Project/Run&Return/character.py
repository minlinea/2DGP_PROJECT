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


character = None

# Character Event
RIGHT_DOWN, RIGHT_UP, LEFT_DOWN, LEFT_UP, JUMP, INSTANT_DOWN, WAIT, LANDING = range(8)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_UP): JUMP,
    (SDL_KEYDOWN, SDLK_DOWN): INSTANT_DOWN,
}


#state

class Ground:
    @staticmethod
    def enter(character, event):
        if event == RIGHT_DOWN:
            character.xspeed += RUN_SPEED_PPS
            character.direction = 1
        elif event == LEFT_DOWN:
            character.xspeed -=  RUN_SPEED_PPS
            character.direction = 0
        elif event == RIGHT_UP:
            if (character.xspeed != 0):
                character.xspeed -= RUN_SPEED_PPS
            character.direction = 1
        elif event == LEFT_UP:
            if (character.xspeed != 0):
                character.xspeed += RUN_SPEED_PPS
            character.direction = 0
        elif event == LANDING:
            character.yspeed = 0
            character.y_axiscount = 0

        pass

    @staticmethod
    def exit(character, event):
        pass

    @staticmethod
    def do(character):
        character.frame = (character.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        character.xpos += character.xspeed * game_framework.frame_time
        character.xpos = clamp(25, character.xpos, 800 - 20)
        if(character.xspeed ==0):
            character.add_event(WAIT)

    @staticmethod
    def draw(character):
        character.image.clip_draw(int(character.frame * 40), character.direction * 0, 40, 80, character.xpos,
                                  character.ypos)
        pass


class Air:

    @staticmethod
    def enter(character, event):
        if event == JUMP:
            character.y_axiscount = 1
        elif event == RIGHT_DOWN:
            character.xspeed += RUN_SPEED_PPS
            character.direction = 1
        elif event == LEFT_DOWN:
            character.xspeed -= RUN_SPEED_PPS
            character.direction = 0
        elif event == RIGHT_UP:
            if (character.xspeed != 0):
                character.xspeed -= RUN_SPEED_PPS
            character.direction = 1
        elif event == LEFT_UP:
            if (character.xspeed != 0):
                character.xspeed += RUN_SPEED_PPS
            character.direction = 0
        elif event == INSTANT_DOWN:
            character.y_axiscount = 81
            if(character.xspeed > 0):
                character.direction = 1
            else:
                character.direction = 0
        pass

    @staticmethod
    def exit(character, event):
        pass

    @staticmethod
    def do(character):
        character.frame = (character.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        if(character.y_axiscount % 6 == 1):
            character.yspeed = -((character.y_axiscount)//6) + 15
            character.y_axiscount += 1
        else:
            character.yspeed = 0
            character.y_axiscount = (character.y_axiscount + 1) % 183
        if(character.y_axiscount == 0):
            character.add_event(LANDING)

        character.ypos += character.yspeed #* game_framework.frame_time

        character.xpos += character.xspeed * game_framework.frame_time
        character.xpos = clamp(25, character.xpos, 800 - 20)
        character.ypos = clamp(0, character.ypos, 600 - 40)
        pass

    @staticmethod
    def draw(character):
        character.image.clip_draw(int(character.frame * 40), character.direction * 0, 40, 80, character.xpos,
                                  character.ypos)
        pass



class Hold:
    @staticmethod
    def enter(character, event):
        if event == WAIT:
            pass
        pass

    @staticmethod
    def exit(character, event):
        pass

    @staticmethod
    def do(character):
        #character.frame = (character.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        character.frame = 0
        pass

    @staticmethod
    def draw(character):
        character.image.clip_draw(int(character.frame * 40), character.direction * 0, 40, 80, character.xpos,
                                  character.ypos)
        pass

class Death:
    def enter(character, event):
        pass

    @staticmethod
    def exit(character, event):
        pass

    @staticmethod
    def do(character):
        character.contact()
        pass

    @staticmethod
    def draw(character):
        character.image.clip_draw(int(character.frame) * 100, character.direction * 100, 40, 80, character.xpos, character.ypos)
        pass




next_state_table = {
    Ground: {RIGHT_DOWN: Ground, LEFT_UP: Ground, RIGHT_UP: Ground, LEFT_DOWN: Ground, JUMP: Air, INSTANT_DOWN: Ground, LANDING : Ground, WAIT : Hold},
    Air: {RIGHT_DOWN: Air, RIGHT_UP: Air, LEFT_UP: Air, LEFT_DOWN: Air, JUMP: Air, INSTANT_DOWN: Air, LANDING : Ground},
    Hold: {LEFT_DOWN: Ground, RIGHT_DOWN: Ground, LEFT_UP: Hold, RIGHT_UP: Hold, JUMP: Air, INSTANT_DOWN: Ground, WAIT : Hold}
}




class Character:
    def __init__(self):
        self.xpos, self.ypos = 150, 280
        self.frame = 0
        self.image = load_image('resource\\character\\animation_sheet_demo.png')
        self.direction = 1
        self.xspeed, self.yspeed = 0, 0
        self.y_axiscount = 0
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


    def crash_tile(self, type):
        if (type == 1):
            if(self.xspeed > 0):
                self.xpos -= 5
                self.xspeed = 0
            elif (self.xspeed < 0):
                self.xpos += 5
                self.xspeed = 0
            self.add_event(WAIT)

    def draw(self):
        self.cur_state.draw(self)
        #draw_rectangle(*self.get_bb())


    def move_instant_down(self):
        self.y_axiscount = 234


    def get_bb(self):
        return self.xpos - 20, self.ypos - 40, self.xpos + 20, self.ypos+40

    def add_event(self, event):
        self.event_que.insert(0, event)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)