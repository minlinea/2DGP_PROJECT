import game_framework
import game_world
import title_state
from pico2d import *

from image import Image

name = "ScoreState"
image = None
font = None

window_right, window_top = 800, 600

scoreboard = None

def enter():
    global scoreboard

    game_world.objects = [[], []]
    
    scoreboard = Image(window_right // 2, window_top // 2, 0,0, 800, 600,
                        'resource\\score_state\\score_board.png')
    game_world.add_object(scoreboard,0)

def exit():
    game_world.clear()



def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if(event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.change_state(title_state)


def draw():
    clear_canvas()

    for game_object in game_world.all_objects():
        game_object.draw()

    update_canvas()


def update():
    pass


def pause():
    pass


def resume():
    pass






