import game_framework
import stage_run
import help_state
from pico2d import *

WINDOW_HEIGHT = 600
pause_image = None
choose_menu = None
choose_menu_pivot_num = 0

def enter():
    global pause_image, choose_menu
    pause_image = load_image('resource\pause_state\pause.png')
    choose_menu = load_image('resource\pause_state\pause_choose_menu.png')



def exit():
    global pause_image, choose_menu
    del(pause_image)
    del(choose_menu)


def update():
    pass


def draw():
    global pause_image, choose_menu
    clear_canvas()
    pause_image.draw(400,300)
    choose_menu.clip_draw(614 * choose_menu_pivot_num,0,614,370,(706+91)/2, WINDOW_HEIGHT - (592+223)/2)
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
                if (window_to_pico_coordinate_system(event.y) < 358 and window_to_pico_coordinate_system(event.y) > 264):
                    choose_menu_pivot_num = 1
                elif(window_to_pico_coordinate_system(event.y) < 240 and window_to_pico_coordinate_system(event.y) > 150):
                    choose_menu_pivot_num = 2
                elif (window_to_pico_coordinate_system(event.y) < 124 and window_to_pico_coordinate_system(
                        event.y) > 34):
                    choose_menu_pivot_num = 3
                else:
                    choose_menu_pivot_num = 0
            else:
                choose_menu_pivot_num = 0
            pass
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if (choose_menu_pivot_num == 1):
                game_framework.pop_state()
            elif (choose_menu_pivot_num ==2):
                game_framework.push_state(help_state)
            elif (choose_menu_pivot_num ==3):
                game_framework.quit()
            pass

def window_to_pico_coordinate_system(num):      # pico 환경과, 윈도우 환경 마우스 좌표 값 조정 함수
    return WINDOW_HEIGHT - 1 - num



def pause(): pass


def resume(): pass




