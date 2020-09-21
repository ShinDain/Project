import helper
from pico2d import *

def handle_events():
    global running
    global delta, speed, Mx, My, target, done, pos
    evts = get_events()
    for e in evts:
        if e.type == SDL_KEYDOWN:
            if e.key == SDLK_ESCAPE:
                running = False
        elif e.type == SDL_QUIT:
            running = False
        elif e.type == SDL_MOUSEBUTTONDOWN:
            Mx, My = e.x, get_canvas_height() - e.y - 1
            if e.button == SDL_BUTTON_LEFT:
                target.append((Mx,My))
                if done == False:
                    speed += 2

                   
open_canvas()
gra = load_image('grass.png')
ch = load_image('run_animation.png')

pos = 400,85    # 현위치
target = [(400,85)]# 목적지 리스트

count = 0       # 목적지 카운트

done = True
fidx = 0
delta = 0, 0    # 이동 거리
speed = 1       # 프레임 당 이동 속도

Mx, My = 0,0    # 마우스 위치   

running = True

while running:
    clear_canvas()
    gra.draw(400,30)
    ch.clip_draw(fidx * 100, 0 , 100,100,pos[0],pos[1])
    update_canvas()

    handle_events()

    delta = helper.delta(pos,target[count],speed)
    pos, done = helper.move_toward(pos,delta,target[count])

    if pos == target[count] and len(target) - count != 1:
        count += 1

    if done == False:
        pos += delta
    else: 
        speed = 1

    fidx = (fidx + 1) % 8
    delay(0.01)

close_canvas()
            
