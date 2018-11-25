import game_framework
import stage_run
import stage_editor
import game_world

from pico2d import *
from music import BGM
from image import Image


name = "TitleState"
title = None
backgroundmusic = None
window_right, window_top = 800, 600


def enter():
    global title, backgroundmusic
    game_world.objects = [[], []]
    title = Image(window_right // 2, window_top // 2, 0, 0, 800, 600, 'resource\\title_state\\title.png')
    game_world.add_object(title, 0)
    backgroundmusic = BGM("title_state")


def exit():
    game_world.clear()
    backgroundmusic.stop()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if(event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(stage_run)
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_p):
                game_framework.change_state(stage_editor)


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()


def update():pass


def pause():pass


def resume():pass
