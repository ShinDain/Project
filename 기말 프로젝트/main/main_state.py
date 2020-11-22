import gfw
from player import Player
from pico2d import *
import gobj
from background import HorzScrollBackground
import all_stage_gen
import camera

canvas_width = 1000
canvas_height = 800

def enter():
    gfw.world.init(['bg','tile','player'])
    global player, bg
    player = Player()
    gfw.world.add(gfw.layer.player, player)

    bg = HorzScrollBackground('Background.png')
    gfw.world.add(gfw.layer.bg, bg)

    all_stage_gen.make_all_map()

    camera.camera_init()

def update():
    global player, bg
    gfw.world.update()
    bg.speed = player.dx * 5

    p_draw_x, p_draw_y, left_gab, bottom_gab = camera.update(player)

    player.set_draw_pos(p_draw_x,p_draw_y)
    for t in gfw.world.objects_at(gfw.layer.tile):
        t.left_gab = left_gab
        t.bottom_gab = bottom_gab
    
def draw():
    gfw.world.draw()
    gobj.draw_collision_box()
    
def handle_event(e):
    global player
    # prev_dx = boy.dx0 
    if e.type == SDL_QUIT:
        gfw.quit()
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            gfw.pop()
        elif e.key == SDLK_7:
            for t in gfw.world.objects_at(gfw.layer.tile):
                gfw.world.remove(t)
            all_stage_gen.make_all_map()

    player.handle_event(e)

def exit():
    pass

if __name__ == '__main__':
    gfw.run_main()
