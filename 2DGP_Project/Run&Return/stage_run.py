import game_framework
import game_world
import title_state
import pause_state
import stage_return
import random
import score_state

from pico2d import *
from stickman import Stickman
from tile import Tile
from music import BGM
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
pause_time = 0
backgroundmusic = None


def load_stage():  # 'save_stage'에 저장되어 있는 타일 파일 로드하여 정보 저장
    global tile, now_stage_num
    file = open("save_stage.txt", 'r')
    rand_stage = random.randint(0, 3)
    horizon_count = 0
    for load_temp in range(0, max_vertical_num * now_stage_num, 1):
        line = file.readline()
    for j in range(0, max_vertical_num, 1):
        line = file.readline()
        for i in range(rand_stage * max_horizontal_num, (rand_stage+1) * max_horizontal_num, 1):
            tile[j][horizon_count].type = int(line[i:i + 1])
            horizon_count += 1
        horizon_count = 0
    line = file.readline()
    if line:
        now_stage_num += 1
    file.close()


def enter():
    global now_stage_num, stage_past_time, font
    font = load_font('ENCR10B.TTF', 32)
    stage_past_time = get_time()
    now_stage_num = 0

    global tile
    tile = [([(Tile(j,i,'run')) for i in range(max_horizontal_num)]) for j in range(max_vertical_num)]
    for j in range(0, max_vertical_num, 1):
            game_world.add_objects(tile[j], 0)
    load_stage()

    global stickman
    stickman = Stickman()
    game_world.add_object(stickman, 1)

    global backgroundmusic
    backgroundmusic = BGM("stage")

def exit():
    backgroundmusic.stop()


def pause():
    pass

def resume():
    global tile, now_stage_num, stage_past_time, pause_time

    pause_time += pause_state.pause_time
    stickman.xspeed = 0



def update():

    for game_object in game_world.all_objects():
        game_object.update()

    center_x, center_y = int(stickman.xpos // 40), int(stickman.ypos // 40)
    center_x_left, center_x_right = clamp(0, center_x - 1, max_horizontal_num - 1), clamp(0, center_x + 1, max_horizontal_num - 1)
    center_y_bottom, center_y_top = clamp(0, center_y - 2, max_vertical_num - 1), clamp(0, center_y + 1, max_vertical_num - 1)


    collide_check = False   #stickman.crash_tile 검사용
    for i in range(center_x_left, center_x_right + 1, 1):
        for j in range (center_y_bottom, center_y_top + 1, 1):
            if (collide_normal_tile(stickman, tile[j][i])):
                #if (tile[j][i].type >= 4):
                    #if (collide_thorn(stickman, tile[j][i], tile[j][i].type)):
                        #stickman.crash_tile(tile[j][i].type, j, i)
                if tile[j][i].type >= 1:
                    stickman.crash_tile(tile[j][i].type, j, i)
                    collide_check = True
    if not collide_check:   #stickman.crash_tile이 안불렸다면
        stickman.crash = False  #stickman.crash 초기화

    if(stickman.opacify >= 1):
        if (limit_time - (get_time() - stage_past_time - pause_time) <= 0):
            game_framework.change_state(stage_return)

        elif (stickman.xpos >= window_right - (stickman.size // 2 + 1)):
            load_stage()
            stickman.xpos = window_left + (stickman.size // 2 + 1)
    else:
        if(stickman.opacify == 0):
            game_framework.change_state(score_state)



def draw():
    clear_canvas()

    for game_object in game_world.all_objects():
        game_object.draw()

    if (stickman.opacify >= 1):
        time = limit_time - (get_time() - stage_past_time - pause_time)
        font.draw(window_right - 80, 30, '[%2.0f]' % time, (255, 255, 255))

    update_canvas()


def handle_events():
    global stickman
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        if (stickman.opacify >= 1):
            if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.push_state(pause_state)

            else:
                stickman.handle_event(event)

def collide_normal_tile(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True

def collide_thorn(a, b, type):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()


    if type == 4:
        center_b = (right_b + left_b) / 2

        dewl = 2 * right_a
        dewr = 80 * (left_b//40)

        templ = 2 * left_a
        tempr = (80 * (right_b//40))
        dew = (((top_b - bottom_b) / (center_b - left_b)) * right_a - (80 * (left_b//40)))
        temp = -((top_b - bottom_b) / (center_b - left_b)) * left_a + (80 * (right_b//40))
        if dew < bottom_a:    #2 * right_a + 40 * tile[x]
            return False
        if temp < bottom_a: #-2 * roght_a +  tile[x+1] * 40
            return False
        if top_a < bottom_b:
            return False
        return True
    else:
        return False