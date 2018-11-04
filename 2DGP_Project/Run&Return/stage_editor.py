import game_framework
import title_state
from pico2d import *


from tile import Tile

tile = None
tile_kind = None
tile_choose = None
imposible_collocate = None

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600

tile_choose_place = [(33,214),(87,214), (33,155),(87,155) , (33,96),(87,96),(33,35),(87,35)]
tile_choose_num = 0
save_count = 0
load_count = 0
click = False

#----------------------------------------게임 오브젝트 클래스--------------------------------------#
class Image:
    def __init__(self, x, y, left, bottom, width, height, title):
        self.x, self.y = x,y
        self.left, self.bottom = left, bottom
        self.width, self.height =  width, height
        self.image = load_image(title)

    def draw(self, x, y):
        self.image.draw(x, y)

    def clip_draw(self, x, y):
        self.image.clip_draw(self.left,self.bottom,self.width, self.height,x,y)


#----------------------------------------게임 오브젝트 클래스--------------------------------------#

#----------------------------------------게임 프레임 워크-------------------------------------------#
def enter():
    global tile, tile_kind, tile_choose, imposible_collocate
    tile = [([(Tile(j,i,'editor')) for i in range(20)]) for j in range(15)]
    tile_choose = Image(tile_choose_place[tile_choose_num][0], tile_choose_place[tile_choose_num][1],
                    0,0, 53+1, 61+1, 'resource\\tile\\tile_choose.png')
    tile_kind = Image((120 / 2), (250 / 2), 0, 0, 120, 250, 'resource\\tile\\tile_kind.png')
    imposible_collocate = Image((120/2), (400/2), 0, 0, 120, 400, 'resource\\tile\imposible_collocate.png')
    pass


def exit():
    global tile, tile_kind, tile_choose, imposible_collocate
    #del(tile)
    del(tile_kind)
    del(tile_choose)
    del(imposible_collocate)


def pause():
    pass


def resume():
    pass


def update():
    pass


def draw():
    clear_canvas()
    for j in range(0, 15, 1):
        for i in range(0, 20, 1):
            tile[j][i].draw()
    imposible_collocate.clip_draw((120 / 2), imposible_collocate.y)
    imposible_collocate.clip_draw(WINDOW_WIDTH - (120 / 2), imposible_collocate.y)
    tile_kind.clip_draw(tile_kind.x, tile_kind.y)
    tile_choose.clip_draw(tile_choose_place[tile_choose_num][0], tile_choose_place[tile_choose_num][1])

    update_canvas()
#----------------------------------------게임 프레임 워크-------------------------------------------#

#----------------------------------------핸들 이벤트---------------------------------------------#
def handle_events():
    global click
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
        elif event.type == SDL_MOUSEBUTTONDOWN or (
                event.type == SDL_MOUSEMOTION and click == True) or event.type == SDL_MOUSEBUTTONUP:
            mouse_xpos, mouse_ypos = event.x, window_to_pico_coordinate_system(event.y)
            click = event_MOUSE(event.type, mouse_xpos, mouse_ypos, click, tile_choose_num)

        elif event.type == SDL_KEYDOWN:
            event_KEYDOWN(event.key)

#-------------------------------------------------마우스 처리관련-------------------------------------------------#
def event_MOUSE(type, x, y, click, tile_type):      # 마우스 처리
    if type == SDL_MOUSEBUTTONDOWN:  # 클릭 시 해당지점 타일 배치
        click = True
        collocate_tile(tile_type, x, y)
    elif type == SDL_MOUSEMOTION and click == True:  # 누른채로 이동하면 해당 이동 구역 전부 타일 배치
        collocate_tile(tile_type, x, y)

    elif type == SDL_MOUSEBUTTONUP:
        click = False  # 마우스 버튼 뗀 순간 마우스모션과 연계 안되게끔
    return click

def collocate_tile(tile_type, mouse_x, mouse_y):     # 마우스 값을 입력 받아 해당된 곳에, 현재 설정된 타일 배치
    global tile
    i = (mouse_x) // 40
    j = (mouse_y) // 40
    tile[j][i].type = tile_type

def window_to_pico_coordinate_system(num):      # pico 환경과, 윈도우 환경 마우스 좌표 값 조정 함수
    return WINDOW_HEIGHT - 1 - num
#-------------------------------------------------마우스 처리관련-------------------------------------------------#

#-------------------------------------------------키보드 처리관련-------------------------------------------------#
def event_KEYDOWN(key):         # 키보드 처리
    global tile_information_kind, tile_choose_num
    if key == SDLK_1:  # 왼쪽 1번째줄 타일 셋
        tile_choose_num = 0
    elif key == SDLK_2:  # 오른쪽 1번째줄 타일 셋
        tile_choose_num = 1
    elif key == SDLK_3:  # 왼쪽 2번째줄 타일 셋
        tile_choose_num = 2
    elif key == SDLK_4:  # 오른쪽 2번째줄 타일 셋
        tile_choose_num = 3
    elif key == SDLK_5:  # 왼쪽 3번째줄 타일 셋
        tile_choose_num = 4
    elif key == SDLK_6:  # 오른쪽 3번째줄 타일 셋
        tile_choose_num = 5
    elif key == SDLK_7:  # 왼쪽 4번째줄 타일 셋
        tile_choose_num = 6
    elif key == SDLK_8:  # 오른쪽 4번째줄 타일 셋
        tile_choose_num = 7
    elif key == SDLK_9:  # 현재 그려진 타일 저장
        save_stage()
    elif key == SDLK_0:  # save_stage.txt에 저장된 타일 로드
        load_stage()
    elif key == SDLK_r:  # 모든 타일 빈타일로 초기화
        clear_stage()


def save_stage():           # 현재까지 그린 정보 저장
    global tile, save_count
    if(save_count>0):
        file = open("save_stage.txt",'a')
    else:
        file = open("save_stage.txt", 'w')
    for j in range(0, 15, 1):
        for i in range(0, 20, 1):
            if ((j >= 6 and j<=9) and ((i>=0 and i<=2) or (i>=17 and i<=19))):  # 생성 불가능 지역 빈 공간
                data = str(0)
            elif ((j <= 5) and ((i>=0 and i<=2) or (i>=17 and i<=19))):     # 생성 불가능 지역 일반 블록 부분
                data = str(1)
            else:
                data = str(tile[j][i].type)     # 생성 불가능 지역이 아니면 저장된 정보 저장
            file.write(data)
        file.write("\n")
    file.close()
    save_count += 1


def clear_stage():          # 타일 초기화, 모든 타일을 빈타일로 만듬
    global tile, save_count, load_count
    for j in range(0, 15, 1):
        for i in range(0, 20, 1):
            tile[j][i].type = 0



def load_stage():  # 'save_stage'에 저장되어 있는 타일 파일 로드하여 정보 저장
    global tile, load_count
    file = open("save_stage.txt", 'r')
    for load_temp in range(0, 15 * load_count, 1):
        line = file.readline()
    for j in range(0, 15, 1):
        line = file.readline()
        for i in range(0, 20, 1):
            tile[j][i].type = int(line[i:i + 1])

    line = file.readline()
    if line:
        load_count += 1
    file.close()


#-------------------------------------------------키보드 처리관련-------------------------------------------------#
#----------------------------------------핸들 이벤트---------------------------------------------#