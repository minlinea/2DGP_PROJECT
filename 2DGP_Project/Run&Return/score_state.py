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
return_main_menu = None
game_exit = None

choose_menu_pivot_num = 0

none_select, return_main, exit = range(3)
choose_menu_type = {none_select : 0, return_main : 1, exit : 2}

def enter():
    global scoreboard, score, pass_run_stage, pass_return_stage, return_main_menu, game_exit

    game_world.objects = [[], []]

    score = load_font('ENCR10B.TTF', 32)
    pass_run_stage = load_font('ENCR10B.TTF', 32)
    pass_return_stage = load_font('ENCR10B.TTF', 32)
    scoreboard = Image(window_right // 2, window_top // 2, 0,0, 800, 600,
                        'resource\\score_state\\score_board.png')
    game_world.add_object(scoreboard,0)

    return_main_menu = Image(window_right/2 - 200, window_top / 6, 270 * 0, 0, 270 - 1, 86,
                        'resource\\score_state\\return_main_menu.png')
    game_world.add_object(return_main_menu, 1)

    game_exit = Image(window_right/2 + 200, window_top / 6, 270 * 0, 0, 270 - 1, 86,
                        'resource\\score_state\\game_exit.png')
    game_world.add_object(game_exit, 1)


def exit():
    game_world.clear()


def handle_events():
    global choose_menu_pivot_num
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEMOTION:
            mouse_pos = event.x, window_to_pico_coordinate_system(event.y)
            return_image_pos = return_main_menu.x, return_main_menu.y
            exit_image_pos = game_exit.x, game_exit.y
            if(collide(return_image_pos, mouse_pos)):
                choose_menu_pivot_num = return_main
            elif (collide(exit_image_pos, mouse_pos)):
                choose_menu_pivot_num = exit
            else:
                choose_menu_pivot_num = none_select


        elif event.type == SDL_MOUSEBUTTONDOWN:
            if (choose_menu_pivot_num == return_main):
                game_framework.change_state(title_state)
            elif (choose_menu_pivot_num == exit):
                game_framework.quit()


def window_to_pico_coordinate_system(num):      # pico 환경과, 윈도우 환경 마우스 좌표 값 조정 함수
    return window_top - 1 - num

def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()

    pass_run_stage_num = stage_run.now_stage_num
    pass_run_stage.draw(window_right // 5, window_top * 4 // 5, 'pass_run_stage : [%2.0f]' %pass_run_stage_num, (255, 255, 255))

    pass_return_stage_num = stage_return.now_stage_num - stage_run.now_stage_num + 1
    pass_return_stage.draw(window_right // 5, window_top * 3 // 5, 'pass_return_stage : [%2.0f]' % pass_return_stage_num, (255, 255, 255))

    if(stage_return.stickman != None):
        run_score = stage_return.stickman.run_distance / PIXEL_PER_METER
    else:
        run_score = stage_run.stickman.run_distance / PIXEL_PER_METER
    score.draw(window_right // 5, window_top * 2 //5 , 'run_distance : [%4.2f]m' % run_score, (255, 255, 255))

    update_canvas()


def update():
    if(choose_menu_pivot_num == none_select):
        return_main_menu.left = (270 - 1) * 0
        game_exit.left = (270 - 1) * 0
    elif(choose_menu_pivot_num == return_main):
        return_main_menu.left = (270-1) * 1
    elif (choose_menu_pivot_num == exit):
        game_exit.left = (270-1) * 1


def pause(): pass


def resume(): pass


def collide(a, b):
    left_a,bottom_a, right_a, top_a  = int(a[0] - 270//2), int(a[1] - 86//2), int(a[0] + 270//2),int(a[1] + 86//2)
    left_b, bottom_b, right_b, top_b = int(b[0] - 5), int(b[1] - 5), int(b[0] +5), int(b[1] + 5)

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True
