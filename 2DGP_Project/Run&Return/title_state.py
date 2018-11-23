import game_framework
import stage_run
import stage_editor
from pico2d import *

from music import BGM

name = "TitleState"
image = None
backgroundmusic = None

def enter():
    global image, backgroundmusic
    image = load_image('resource\\title_state\\title.png')
    backgroundmusic = BGM("title_state")

def exit():
    global image
    del(image)
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
    image.draw(400,300)
    update_canvas()







def update():
    pass


def pause():
    pass


def resume():
    pass






