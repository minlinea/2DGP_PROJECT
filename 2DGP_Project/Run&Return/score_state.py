import game_framework
import game_world
import title_state
import stage_return
from pico2d import *

from image import Image

name = "ScoreState"
image = None
font = None

window_right, window_top = 800, 600

scoreboard = None

score = None

def enter():
    global scoreboard, score

    game_world.objects = [[], []]

    score = load_font('ENCR10B.TTF', 32)
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

    run_score = stage_return.stickman.run_distance
    score.draw(window_right // 2, window_top //2 , 'score : [%4.2f]' % run_score, (255, 255, 255))

    update_canvas()


def update():
    pass


def pause():
    pass


def resume():
    pass






