import game_framework
import pause_state
from pico2d import *

WINDOW_HEIGHT = 600
pause_image = None
choose_menu = None
choose_menu_pivot_num = 0

def enter():
    global pause_image
    pause_image = load_image('pause.png')



def exit():
    global pause_image
    del(pause_image)


def update():
    pass


def draw():
    global pause_image
    clear_canvas()
    pause_image.draw(400,300)
    update_canvas()




def handle_events():
    global choose_menu_pivot_num
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.pop_state()

def window_to_pico_coordinate_system(num):      # pico 환경과, 윈도우 환경 마우스 좌표 값 조정 함수
    return WINDOW_HEIGHT - 1 - num



def pause(): pass


def resume(): pass




