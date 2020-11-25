import gfw
from player import Player
from pico2d import *
import gobj
from background import HorzScrollBackground
import all_stage_gen
import camera
import whip
import objects
import collision 
import ui

canvas_width = 1000
canvas_height = 800

def enter():
    gfw.world.init(['bg','tile','object','score_object','monster', 'whip','player','ui'])
    global player, bg, player_ui, main_bgm, black_canvas, black_pos
    
    bg = HorzScrollBackground('Background.png')
    gfw.world.add(gfw.layer.bg, bg)
    
    (e_x,e_y), (o_x,o_y) = all_stage_gen.make_all_map()
    e_x,e_y,o_x,o_y = change_to_screen(e_x,e_y, o_x,o_y)
    player = Player((e_x + 32,e_y + 32))
    gfw.world.add(gfw.layer.player, player)

    clear_in_out(e_x,e_y,o_x,o_y)
    ui.load()
    objects.load()
    camera.camera_init()

    player_ui = ui.Ui(player)
    gfw.world.add(gfw.layer.ui, player_ui)

    black_canvas = gfw.image.load('res/black.png')
    black_pos = 0, get_canvas_height() + 600

    main_bgm = load_music('res/stage_bgm.mp3')
    main_bgm.set_volume(20)
    main_bgm.repeat_play()

    box = objects.Something(player.pos, 'treasure_box')
    gfw.world.add(gfw.layer.object,box)

def update():
    global player, bg, player_ui

    collision.collide_check(player)
    player_ui.set_count(player)

    gfw.world.update()
    bg.speed = player.dx * 5

    p_draw_x, p_draw_y, left_gab, bottom_gab = camera.update(player)

    player.set_draw_pos((p_draw_x,p_draw_y))
    for layer in range(gfw.layer.tile, gfw.layer.monster + 1):
        for obj in gfw.world.objects_at(layer):
            obj.left_gab = left_gab
            obj.bottom_gab = bottom_gab

    p_x, p_y = player.draw_pos
    for i in gfw.world.objects_at(gfw.layer.whip):
        i.pos = (p_x, p_y)

    global black_canvas, black_pos
    b_x, b_y = black_pos
    if player.stage_clear == True:
        if b_y > 0:
            b_y -= 10
        else:
            reset()
    else:
        if b_y < get_canvas_height():
            b_y += 10
    black_pos = b_x, b_y

    if player.life == 0:
        main_bgm.stop()
    if player.death_time < 0:
        main_bgm.repeat_play()
        player.life = 4
        reset()

def draw():
    global black_canvas
    gfw.world.draw()
    gobj.draw_collision_box()
    black_canvas.draw_to_origin(*black_pos,get_canvas_width(), get_canvas_height())

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
    global main_bgm
    del main_bgm

def reset():
    for layer in range(gfw.layer.tile, gfw.layer.whip + 1):
        gfw.world.clear_at(layer)

    (e_x,e_y), (o_x,o_y) = all_stage_gen.make_all_map()
    e_x,e_y,o_x,o_y = change_to_screen(e_x,e_y, o_x,o_y)
    player.init((e_x + 32,e_y + 32))

    clear_in_out(e_x,e_y,o_x,o_y)

def clear_in_out(x1,y1,x2,y2):
    for t in gfw.world.objects_at(gfw.layer.tile):
        if t.left == x1 and t.bottom == y1 and t.name is not 'entrance':
            gfw.world.remove(t)
        elif t.left == x2 and t.bottom == y2 and t.name is not 'exit':
            gfw.world.remove(t)

def change_to_screen(x1,y1,x2,y2):
    x1 = x1 * 640 + 320
    y1 = y1 * 512 + 192
    x2 = x2 * 640 + 320
    y2 = y2 * 512 + 192
    return x1,y1,x2,y2

if __name__ == '__main__':
    gfw.run_main()
