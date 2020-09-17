from pico2d import *

open_canvas()

gra = load_image('grass.png')
ch = load_image('animation_sheet.png')

x = 0 
frame_index = 0 # 소스 이미지
action = 3
while x < 800:
    clear_canvas()
    gra.draw(400, 30)
    ch.clip_draw(100 * frame_index,100 * action,100,100,x, 85) # 이미지를 잘라서 그린다.
    update_canvas() # 백퍼퍼에 있는 내용을 프론트 버퍼로 옮긴다.

    get_events() # 쌓인 이벤트를 처리

    x += 2
    # frame_index += 1
    # if frame_index >= 8: frame_index = 0
    # cpu는 분기를 싫어하기 때문에 아래 코드가 더 유용하다. -> 분기를 최소화하는 것이 좋다.
    frame_index = (frame_index + 1) % 8

    if x % 100 == 0:
        action = (action + 1) % 4

    delay(0.02)
   

delay(1) 

close_canvas()


# game lopp
# - logic = update
# - 
# - now : 프론트 버퍼에 작업