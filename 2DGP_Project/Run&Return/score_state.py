import game_framework
import stage_run
import stage_editor
from pico2d import *


name = "ScoreState"
image = None
font = None

def enter():
    global image
    image = load_image('resource\\score_state\\score_board.png')


def exit():
    global image
    del(image)


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if(event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()


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






