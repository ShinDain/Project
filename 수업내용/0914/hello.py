from pico2d import *

open_canvas()

gra = load_image('grass.png')
ch = load_image('character.png')

gra.draw_now(400, 30)
for x in range(100, 500+ 1, 100):
    for y in range(150, 550 + 1, 100):
        ch.draw_now(x,y)

delay(2)

clear_canvas_now()

delay(2)

close_canvas()
