import game_framework
import game_world
import title_state
import pause_state
import stage_run
import score_state
import random
from pico2d import *
from stickman import Stickman
from tile import Tile
from music import BGM
name = "StageReturn"

stickman =None
tile =None
now_stage_num = 0
max_vertical_num, max_horizontal_num = 15, 20
window_top, window_right = 600, 800
window_left, window_bottom = 0,0
limit_time = 5
stage_past_time = 0
backgroundmusic = None
font = None
pause_time = 0.0

DIE, OVER_LIMIT_TIME, CLEAR, NONE_EVENT  = range(4)
end_judgement = {DIE : 0, OVER_LIMIT_TIME : 1, CLEAR : 2, NONE_EVENT : 3}
pass_score_state = DIE

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
    global stickman, tile, now_stage_num, stage_past_time, font, backgroundmusic, pause_time

    font = load_font('ENCR10B.TTF', 32)

    stage_past_time = get_time() - stage_run.pause_time
    pause_time = stage_run.pause_time

    now_stage_num = stage_run.now_stage_num-1

    stickman = stage_run.stickman
    stickman.image = load_image('resource\\character\\stage_return_animation_sheet.png')

    tile = stage_run.tile
    for i in range(max_vertical_num):
        for j in range(max_horizontal_num):
            tile[i][j].image = load_image('resource\\tile\\stage_return_tile_kind.png')

    backgroundmusic = BGM("stage")


def exit():
    game_world.clear()
    backgroundmusic.stop()

def pause():
    pass


def resume():
    global tile, now_stage_num, stage_past_time, pause_time

    pause_time += pause_state.pause_time
    stickman.xspeed = 0



def update():
    global pass_score_state

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
                    pass_score_state = DIE
    if not collide_check:   #stickman.crash_tile이 안불렸다면
        stickman.crash = False  #stickman.crash 초기화

    if (stickman.opacify >= 1):
        if (limit_time - (get_time() - stage_past_time - pause_time) <= 0):
            if(now_stage_num + 1 - 2 * stage_run.now_stage_num < 0):
                stickman.external_add_event("DIE")
                pass_score_state = OVER_LIMIT_TIME
            else:
                pass_score_state = CLEAR
                game_framework.change_state(score_state)

        elif (stickman.xpos <= window_left + (stickman.size // 2)):
            load_stage()
            stickman.xpos = window_right - (stickman.size // 2)
    else:
        if (stickman.opacify == 0):
            game_framework.change_state(score_state)


def draw():
    clear_canvas()

    for game_object in game_world.all_objects():
        game_object.draw()

    if (stickman.opacify >= 1):
        time = limit_time - (get_time() - stage_past_time - pause_time)
        font.draw(window_right - 80, 30, '[%2.0f]' % time, (0, 0, 0))

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
            elif event.type == SDL_KEYDOWN and event.key == SDLK_z:
                game_framework.change_state(score_state)
            else:
                stickman.handle_event(event)

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True