import game_framework

from pico2d import *


class BGM:

    def __init__(self, state):
        if(state == "title_state"):
            self.bgm = load_music('sound\\title_state\\BGM.mp3')
        elif (state == "stage"):
            self.bgm = load_music('sound\\stage\\BGM.mp3')
        self.bgm.set_volume(64)
        self.bgm.repeat_play()

    def stop(self):
        self.bgm.stop()


class Effect:

    def __init__(self, type):
        if (type == 'death'):
            self.effect = load_wav('sound\\character\\death.wav')
        if(type == 'jump'):
            self.effect = load_wav('sound\\character\\jump.wav')
        self.effect.set_volume(96)

    def play(self):
        self.effect.play()

    def stop(self):
        self.effect.stop()