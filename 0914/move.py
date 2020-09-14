from pico2d import *

open_canvas()

gra = load_image('grass.png')
ch = load_image('character.png')

x = 0 
while x < 800:
    clear_canvas()
    gra.draw(400, 30)
    ch.draw(x, 85)
    update_canvas() # 백퍼퍼에 있는 내용을 프론트 버퍼로 옮긴다.
    x += 2
    delay(0.02)
   

delay(1) 

close_canvas()


# game lopp
# - logic = update
# - 
# - now : 프론트 버퍼에 작업