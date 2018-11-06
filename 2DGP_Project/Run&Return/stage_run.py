import game_framework
import game_world
import title_state
import pause_state
from pico2d import *



from character import Character
from tile import Tile

name = "StageRun"

character =None
tile =None
stage_count = 0




def load_stage():  # 'save_stage'에 저장되어 있는 타일 파일 로드하여 정보 저장
    global tile, stage_count
    file = open("save_stage.txt", 'r')
    for load_temp in range(0, 15 * stage_count, 1):
        line = file.readline()
    for j in range(0, 15, 1):
        line = file.readline()
        for i in range(0, 20, 1):
            tile[j][i].type = int(line[i:i + 1])

    line = file.readline()
    if line:
        stage_count += 1
    file.close()



def enter():
    global character, tile, stage_count
    stage_count = 0
    character = Character()
    tile = [([(Tile(j,i,'run')) for i in range(20)]) for j in range(15)]
    for j in range(0, 15, 1):
            game_world.add_objects(tile[j], 0)
    load_stage()
    game_world.add_object(character, 0)


def exit():
    game_world.remove_object(0)
    game_world.remove_object(1)



def pause():
    pass


def resume():
    pass


def update():

    for game_object in game_world.all_objects():
        game_object.update()
    for i in range(15):
        for tiles in tile:
            if (collide(character, tiles[i])):
                if(tiles[i].type != 0):
                    character.crash_tile(tiles[i].type)

    if(character.opacify == 0):
        game_framework.change_state(title_state)

    if(character.xpos >= 750):
        load_stage()
        character.xpos = 700


def draw():
    clear_canvas()

    for game_object in game_world.all_objects():
        game_object.draw()

    update_canvas()


def handle_events():
    global character
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
            character.handle_event(event)
# --------------------------------------- 키보드 입력 처리----------------------------------------------------#

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True


