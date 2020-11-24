import gfw
from player import Player
from pico2d import *
import gobj
from background import HorzScrollBackground
import all_stage_gen
import camera
import whip

canvas_width = 1000
canvas_height = 800

def enter():
    gfw.world.init(['bg','tile','object', 'whip','player'])
    global player, bg
    
    bg = HorzScrollBackground('Background.png')
    gfw.world.add(gfw.layer.bg, bg)
    
    (e_x,e_y), (o_x,o_y) = all_stage_gen.make_all_map()

    e_x = e_x * 640 + 320
    e_y = e_y * 512 + 192
    o_x = o_x * 640 + 320
    o_y = o_y * 512 + 192
    player = Player((e_x + 32,e_y + 32))
    gfw.world.add(gfw.layer.player, player)

    for t in gfw.world.objects_at(gfw.layer.tile):
        if t.left == e_x and t.bottom == e_y and t.name is not 'entrance':
            gfw.world.remove(t)
        elif t.left == o_x and t.bottom == o_y and t.name is not 'exit':
            gfw.world.remove(t)

    camera.camera_init()

def update():
    global player, bg
    gfw.world.update()
    bg.speed = player.dx * 5

    p_draw_x, p_draw_y, left_gab, bottom_gab = camera.update(player)

    player.set_draw_pos((p_draw_x,p_draw_y))
    for layer in range(gfw.layer.tile, gfw.layer.object + 1):
        for obj in gfw.world.objects_at(layer):
            obj.left_gab = left_gab
            obj.bottom_gab = bottom_gab

    p_x, p_y = player.draw_pos
    for i in gfw.world.objects_at(gfw.layer.whip):
        i.pos = (p_x, p_y)

def reset():
    for layer in range(gfw.layer.tile, gfw.layer.whip + 1):
        gfw.world.clear_at(layer)

    (e_x,e_y), (o_x,o_y) = all_stage_gen.make_all_map()

    e_x = e_x * 640 + 320
    e_y = e_y * 512 + 192
    o_x = o_x * 640 + 320
    o_y = o_y * 512 + 192
    player.init((e_x + 32,e_y + 32))

    for t in gfw.world.objects_at(gfw.layer.tile):
        if t.left == e_x and t.bottom == e_y and t.name is not 'entrance':
            gfw.world.remove(t)
        elif t.left == o_x and t.bottom == o_y and t.name is not 'exit':
            gfw.world.remove(t)

def draw():
    gfw.world.draw()
    gobj.draw_collision_box()
    
def handle_event(e):
    x, y = 0,0
    # prev_dx = boy.dx0 
    if e.type == SDL_QUIT:
        gfw.quit()
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            gfw.pop()
        elif e.key == SDLK_7:
            reset()

    player.handle_event(e)

def exit():
    pass

if __name__ == '__main__':
    gfw.run_main()
