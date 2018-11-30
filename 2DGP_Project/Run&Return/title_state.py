import game_framework
import stage_run
import stage_editor
import game_world

from pico2d import *
from music import BGM
from image import Image

window_right, window_top = 800, 600

name = "TitleState"
title = None
backgroundmusic = None

game_start = None
game_exit = None

choose_menu_pivot_num = 0

none_select, start, exit = range(3)
choose_menu_type = {none_select : 0, start : 1, exit : 2}

def enter():
    global title, backgroundmusic, game_start, game_exit
    game_world.objects = [[], []]
    title = Image(window_right // 2, window_top // 2, 0, 0, 800, 600, 'resource\\title_state\\title.png')
    game_world.add_object(title, 0)
    backgroundmusic = BGM("title_state")

    game_start = Image(window_right / 2 - 200, window_top / 6, 270 * 0, 0, 270 - 1, 84,
                             'resource\\title_state\\game_start.png')
    game_world.add_object(game_start, 1)

    game_exit = Image(window_right / 2 + 200, window_top / 6, 270 * 0, 0, 270 - 1, 84,
                      'resource\\title_state\\game_exit.png')
    game_world.add_object(game_exit, 1)

def exit():
    game_world.clear()
    backgroundmusic.stop()


def handle_events():
    global choose_menu_pivot_num
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if (choose_menu_pivot_num == start):
                game_framework.change_state(stage_run)
            elif (choose_menu_pivot_num == exit):
                game_framework.quit()

        else:
            if(event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_p):
                game_framework.change_state(stage_editor)

            mouse_pos = event.x, window_to_pico_coordinate_system(event.y)
            game_start_pos = game_start.x, game_start.y
            exit_image_pos = game_exit.x, game_exit.y

            if (collide(game_start_pos, mouse_pos)):
                choose_menu_pivot_num = start
            elif (collide(exit_image_pos, mouse_pos)):
                choose_menu_pivot_num = exit
            else:
                choose_menu_pivot_num = none_select

def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()


def update():
    global choose_menu_pivot_num
    if (choose_menu_pivot_num == none_select):
        game_start.left = (270 - 1) * 0
        game_exit.left = (270 - 1) * 0
    elif (choose_menu_pivot_num == start):
        game_start.left = (270 - 1) * 1
    elif (choose_menu_pivot_num == exit):
        game_exit.left = (270 - 1) * 1


def pause():pass


def resume():pass


def window_to_pico_coordinate_system(num):      # pico 환경과, 윈도우 환경 마우스 좌표 값 조정 함수
    return window_top - 1 - num

def collide(a, b):
    left_a,bottom_a, right_a, top_a  = int(a[0] - 270//2), int(a[1] - 84//2), int(a[0] + 270//2),int(a[1] + 84//2)
    left_b, bottom_b, right_b, top_b = int(b[0] - 5), int(b[1] - 5), int(b[0] +5), int(b[1] + 5)

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True