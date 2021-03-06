import game_framework
import stage_run
import game_world

from pico2d import *
from image import Image


pause_image = None
choose_menu = None

pause_time = 0.0
choose_menu_pivot_num = 0
window_top, window_right = 600, 800

none_select, resume, exit = range(3)
choose_menu_type = {none_select : 0, resume : 1, exit : 2}


def enter():
    global pause_image, choose_menu, pause_time

    pause_time = get_time()
    pause_image = Image(window_right // 2, window_top // 2, 0, 0, 800, 600, 'resource\pause_state\pause.png')
    game_world.add_object(pause_image, 1)

    choose_menu = Image(window_right - (592+223)/2, window_top / 3, 614 * 0,0,614,370,
                        'resource\pause_state\pause_choose_menu.png')
    game_world.add_object(choose_menu, 1)


def exit():
    global pause_time
    game_world.remove_object(pause_image)
    game_world.remove_object(choose_menu)
    pause_time = get_time() - pause_time

def update():
    if(choose_menu_pivot_num == none_select):
        choose_menu.left = 614 * 0
    elif(choose_menu_pivot_num == resume):
        choose_menu.left = 614 * 1
    elif (choose_menu_pivot_num == exit):
        choose_menu.left = 614 * 3


def draw():
    clear_canvas()

    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()


def handle_events():
    global choose_menu_pivot_num
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.pop_state()

        elif event.type == SDL_MOUSEMOTION:
            if(event.x < 535 and event.x > 265):
                if (window_to_pico_coordinate_system(event.y) < 358 and  window_to_pico_coordinate_system(event.y) > 264):
                    choose_menu_pivot_num = resume
                elif (window_to_pico_coordinate_system(event.y) < 124 and window_to_pico_coordinate_system(
                        event.y) > 34):
                    choose_menu_pivot_num = exit
                else:
                    choose_menu_pivot_num = none_select
            else:
                choose_menu_pivot_num = none_select

        elif event.type == SDL_MOUSEBUTTONDOWN:
            if (choose_menu_pivot_num == resume):
                game_framework.pop_state()
            elif (choose_menu_pivot_num ==exit):
                game_framework.quit()


def window_to_pico_coordinate_system(num):      # pico 환경과, 윈도우 환경 마우스 좌표 값 조정 함수
    return window_top - 1 - num


def pause(): pass


def resume(): pass




