import game_framework
import game_world
import title_state
import stage_run
import stage_return
from pico2d import *

from image import Image

PIXEL_PER_METER = (10.0 / 0.3) # 10pixel 30cm

name = "ScoreState"
window_right, window_top = 800, 600

scoreboard = None
score = None
pass_run_stage = None
pass_return_stage = None


def enter():
    global scoreboard, score, pass_run_stage, pass_return_stage

    game_world.objects = [[], []]

    score = load_font('ENCR10B.TTF', 32)
    pass_run_stage = load_font('ENCR10B.TTF', 32)
    pass_return_stage = load_font('ENCR10B.TTF', 32)
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

    pass_run_stage_num = stage_run.now_stage_num - 1
    pass_run_stage.draw(window_right // 4, window_top * 3 // 4, 'pass_run_stage : [%2.0f]' %pass_run_stage_num, (255, 255, 255))

    pass_return_stage_num = stage_return.now_stage_num - stage_run.now_stage_num
    pass_return_stage.draw(window_right // 4, window_top * 2 // 4, 'pass_return_stage : [%2.0f]' % pass_return_stage_num, (255, 255, 255))

    run_score = stage_return.stickman.run_distance / PIXEL_PER_METER
    score.draw(window_right // 4, window_top //4 , 'run_distance : [%4.2f]m' % run_score, (255, 255, 255))

    update_canvas()


def update():
    pass


def pause():
    pass


def resume():
    pass






