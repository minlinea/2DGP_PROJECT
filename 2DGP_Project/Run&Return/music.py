import game_framework

from pico2d import *


class BGM:

    def __init__(self):
        self.bgm = load_music('sound\\BGM.mp3')
        self.bgm.set_volume(64)
        self.bgm.repeat_play()

class Effect:

    def __init__(self):
        self.effect = load_wav('pickup.wav')
        self.effect.set_volume(64)

    def play(self):
        self.effect.play()