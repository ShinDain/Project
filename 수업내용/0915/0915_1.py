# game logic -> update
# rendering -> drawing

# 입력 처리
# 이벤트 드리블 -> 직접관여 x 특정 상황발생시 작성한 코드 작동
# 이벤트 폴링 -> 직접관여 
# get_events() : pico2d 제공함수, 주기적으로 호출해줘야함 
# 이벤트큐를 비우는 작업

# 속성 + 행위 = encapsulation(캡슐화, 객체)

from pico2d import *

def handle_events():
    global running   # 함수 내에서 변수를 읽는 경우에는 상관이 없지만,
                     # 쓸 경우에는 반드시 global 지정을 해주어야 한다.
                     # 로컬로 받아들여서 지정안하면 안써짐
    global dx, x, y
    evts = get_events()
    for e in evts:
        if e.type == SDL_KEYDOWN:
            if e.key == SDLK_ESCAPE:
                running = False
            elif e.key == SDLK_LEFT:
                dx -= 1
            elif e.key == SDLK_RIGHT:
                dx += 1
            elif e.key == SDLK_SPACE:
                dx = 0
            print('keydown' ,dx)
        elif e.type == SDL_KEYUP:
            if e.key == SDLK_LEFT:
                dx += 1
            elif e.key == SDLK_RIGHT:
                dx -= 1
            print('keydown' ,dx)
        elif e.type == SDL_QUIT:
            running = False
        elif e.type == SDL_MOUSEMOTION:
            x,y = e.x,get_canvas_height() - e.y - 1

open_canvas()
gra = load_image('grass.png')
ch = load_image('run_animation.png')

x, y = 400,85
fidx = 0
dx = 0

running = True

while running:
    clear_canvas()
    gra.draw(400,30)
    ch.clip_draw(fidx * 100, 0 , 100,100,x,y)
    update_canvas()

    handle_events()
    
    x += dx

    fidx = (fidx + 1) % 8
    delay(0.01)

close_canvas()
