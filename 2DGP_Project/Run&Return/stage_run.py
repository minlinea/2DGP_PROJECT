import game_framework
import game_world
import title_state
import pause_state
import stage_return
from pico2d import *



from stickman import Stickman
from tile import Tile

name = "StageRun"

stickman =None
tile =None
now_stage_num = 0
max_vertical_num, max_horizontal_num = 15, 20
window_top, window_right = 600, 800
window_left, window_bottom = 0, 0
stage_past_time = 0
limit_time = 5
font = None




def load_stage():  # 'save_stage'에 저장되어 있는 타일 파일 로드하여 정보 저장
    global tile, now_stage_num
    file = open("save_stage.txt", 'r')
    for load_temp in range(0, max_vertical_num * now_stage_num, 1):
        line = file.readline()
    for j in range(0, max_vertical_num, 1):
        line = file.readline()
        for i in range(0, max_horizontal_num, 1):
            tile[j][i].type = int(line[i:i + 1])

    line = file.readline()
    if line:
        now_stage_num += 1
    file.close()



def enter():
    global stickman, tile, now_stage_num, stage_past_time, font
    font = load_font('ENCR10B.TTF', 32)
    stage_past_time = get_time()
    game_world.objects = [[], []]
    now_stage_num = 0
    stickman = Stickman()
    tile = [([(Tile(j,i,'run')) for i in range(max_horizontal_num)]) for j in range(max_vertical_num)]
    for j in range(0, max_vertical_num, 1):
            game_world.add_objects(tile[j], 0)
    load_stage()
    game_world.add_object(stickman, 1)


def exit():
    game_world.clear()


def pause():
    pass


def resume():
    pass


def update():

    for game_object in game_world.all_objects():
        game_object.update()

    center_x, center_y = int(stickman.xpos // 40), int(stickman.ypos // 40)
    center_x_left, center_x_right = clamp(0, center_x - 1, max_horizontal_num - 1), clamp(0, center_x + 1, max_horizontal_num - 1)
    center_y_bottom, center_y_top = clamp(0, center_y - 2, max_vertical_num - 1), clamp(0, center_y + 1, max_vertical_num - 1)


    collide_check = False   #stickman.crash_tile 검사용
    for i in range(center_x_left, center_x_right + 1, 1):
        for j in range (center_y_bottom, center_y_top + 1, 1):
            if (collide(stickman, tile[j][i])):
                if (tile[j][i].type != 0):
                    stickman.crash_tile(tile[j][i].type, j, i)
                    collide_check = True
    if not collide_check:   #stickman.crash_tile이 안불렸다면
        stickman.crash = False  #stickman.crash 초기화

    if(stickman.opacify == 0):
        game_framework.change_state(title_state)
    elif(limit_time - (get_time() - stage_past_time) <= 0):
        game_framework.change_state(stage_return)
    if(stickman.xpos >= window_right - (stickman.size//2 + 1)):
        load_stage()
        stickman.xpos = window_left + (stickman.size//2 + 1) #임시 설정

def draw():
    clear_canvas()

    for game_object in game_world.all_objects():
        game_object.draw()

    time = limit_time - (get_time() - stage_past_time)
    font.draw(window_right - 80, 30, '[%2.0f]' % time, (255, 255, 255))

    update_canvas()


def handle_events():
    global stickman
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
#------------------------------------------- 마우스 처리----------------------------------------------------#

# ------------------------------------------- 마우스 처리----------------------------------------------------#

# --------------------------------------- 키보드 입력 처리----------------------------------------------------#
        else:
            stickman.handle_event(event)
# --------------------------------------- 키보드 입력 처리----------------------------------------------------#

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True