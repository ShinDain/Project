from pico2d import *
import gfw

Tile = []
TileSelect = []
Select = 0    # 공백, 기본, 가시, 사다리, 화살, 미는 블록  : 0-5

def enter():
    global image
    image = load_image('res/tileset.png')

    global font
    font = gfw.font.load('res/segoeprb.ttf', 40)

def update():
    pass

def draw():
    global Select
    global Mx
    global My

    for i in range(4):
        image.clip_draw(128,1664,128,128, 1100,100 + (200 * i),200,200)
    for i in range(6):
        image.clip_draw(128,1536,128,128,1100,750 - i * 100, 90,90)
    image.clip_draw(0,1664,128,128,1100,100, 200,100)
    font.draw(1050, 100, 'Save')
    image.clip_draw(0,1984,64,64,1100,750) # 미는 블록
    image.clip_draw(64,1984,64,64,1100,650) # 화살 블록
    image.clip_draw(128,1984,64,64,1100,550) # 사다리
    image.clip_draw(320,1600,64,64,1100,450) # 가시 
    image.clip_draw(192,1920,64,64,1100,350) # 기본 블록
    image.clip_draw(256,1984,64,64,1100,250) # 공백

    if Select == 0:
        image.clip_draw(256,1984,64,64,Mx,My) # 공백
    elif Select == 1:
        image.clip_draw(192,1920,64,64,Mx,My) # 기본 블록
    elif Select == 2:
        image.clip_draw(320,1600,64,64,Mx,My) # 가시 
    elif Select == 3:
        image.clip_draw(128,1984,64,64,Mx,My) # 사다리
    elif Select == 4:
        image.clip_draw(64,1984,64,64,Mx,My) # 화살 블록
    elif Select == 5:
        image.clip_draw(0,1984,64,64,Mx,My) # 미는 블록

    for i in range(len(Tile)):
        if TileSelect[i] == 1: # 기본
           image.clip_draw(192,1920,64,64, *Tile[i],100,100)
        elif TileSelect[i] == 2: # 가시
            image.clip_draw(320,1600,64,64,*Tile[i],100,100)
        elif TileSelect[i] == 3: # 사다리
            image.clip_draw(128,1984,64,64,*Tile[i],100,100)
        elif TileSelect[i] == 4: # 화살
            image.clip_draw(64,1984,64,64,*Tile[i],100,100)
        elif TileSelect[i] == 5: # 미는
            image.clip_draw(0,1984,64,64,*Tile[i],100,100)

def handle_event(e):
    global Tile
    global Select

    if e.type == SDL_QUIT:
        gfw.quit()
    elif (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
        gfw.quit()
    if (e.type, e.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT):
        if e.x < 1000:
            Tx = e.x // 100
            Ty = (get_canvas_height() - e.y - 1) // 100
            Tile.append((Tx * 100 + 50,Ty * 100 + 50))
            TileSelect.append(Select)
        else:
            tmpy = get_canvas_height() - e.y - 1
            if tmpy > 700 and tmpy < 800:
                Select = 5 # 미는
            elif tmpy > 600 and tmpy < 700:
                Select = 4 # 화살
            elif tmpy > 500 and tmpy < 600:
                Select = 3 # 사다리
            elif tmpy > 400 and tmpy < 500:
                Select = 2 # 가시 
            elif tmpy > 300 and tmpy < 400:
                Select = 1 # 기본
            elif tmpy > 200 and tmpy < 300:
                Select = 0 # 공백
    if e.type == SDL_MOUSEMOTION:
        global Mx
        global My
        Mx = e.x
        My = get_canvas_height() - e.y - 1
def exit():
    global image
    del image

def pause():
    pass
def resume():
    pass
    
if __name__ == '__main__':
    gfw.run_main()

def save():
    pass


# 만든 맵 저장 구현 