import gfw
from player import Player
from pico2d import *
import gobj
from background import HorzScrollBackground
import random
import all_stage_gen
import camera
import objects
import collision
import monster
import tile
import ui
import ufo

canvas_width = 1200
canvas_height = 800

def enter():
    gfw.world.init(['bg','tile','object','score_object','monster', 'effect','ufo','whip','player','ui'])
    global player, bg, player_ui, main_bgm, ufo_bgm, black_canvas, black_pos, stage_time, all_time, ufo_count
    
    bg = HorzScrollBackground('Background.png')
    gfw.world.add(gfw.layer.bg, bg)

    stage_time = 0
    all_time = 0
    ufo_count = 0
    
    load_all()

    (e_x,e_y), (o_x,o_y) = all_stage_gen.make_all_map()
    e_x,e_y,o_x,o_y = change_to_screen(e_x,e_y, o_x,o_y)
    player = Player((e_x + 32,e_y + 32))
    gfw.world.add(gfw.layer.player, player)

    clear_in_out(e_x,e_y,o_x,o_y)

    player_ui = ui.Ui(player)
    gfw.world.add(gfw.layer.ui, player_ui)

    black_canvas = gfw.image.load('res/black.png')
    black_pos = 0, 0

    main_bgm = load_music('res/main_bgm.mp3')
    main_bgm.set_volume(10)
    main_bgm.repeat_play()

    ufo_bgm = load_music('res/ufo_bgm.mp3')
    ufo_bgm.set_volume(10)

    global fade_out_sound
    fade_out_sound = load_wav('res/wav/fadeout.wav')

def update():
    global player, bg, player_ui, ufo_count, stage_time, all_time

    stage_time += gfw.delta_time
    all_time += gfw.delta_time

    collision.collide_check(player)
    player_ui.set_count(player)

    gfw.world.update()
    bg.speed = player.dx * 5

    p_draw_x, p_draw_y, left_gab, bottom_gab = camera.update(player)

    player.set_draw_pos((p_draw_x,p_draw_y))
    for layer in range(gfw.layer.tile, gfw.layer.ufo + 1):
        for obj in gfw.world.objects_at(layer):
            obj.set_draw_pos(left_gab,bottom_gab)

    p_x, p_y = player.draw_pos
    for i in gfw.world.objects_at(gfw.layer.whip):
        i.pos = (p_x, p_y)

    ufo_maker()
    death_check()
    fade_in_out()

def draw():
    global black_canvas
    gfw.world.draw()
    #gobj.draw_collision_box()
    black_canvas.draw_to_origin(*black_pos,get_canvas_width(), get_canvas_height())

def handle_event(e):
    x, y = 0,0
    # prev_dx = boy.dx0 
    if e.type == SDL_QUIT:
        gfw.quit()
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            gfw.pop()
        elif e.key == SDLK_7 and player.death_time == 8:
            player.life = 5
            player.score = 0
            player.boom_count = 4
            player.rope_count = 4
            reset()

    player.handle_event(e)

def exit():
    global main_bgm, ufo_bgm
    del main_bgm
    del ufo_bgm

def load_all():
    ufo.load()
    ui.load()
    objects.load()
    monster.load()
    tile.load()
    camera.camera_init()

def reset():
    global stage_time, ufo_count
    for layer in range(gfw.layer.tile, gfw.layer.whip + 1):
        gfw.world.clear_at(layer)

    (e_x,e_y), (o_x,o_y) = all_stage_gen.make_all_map()
    e_x,e_y,o_x,o_y = change_to_screen(e_x,e_y, o_x,o_y)
    player.init((e_x + 32,e_y + 32))

    stage_time = 0
    ufo_count = 0 
    fade_out_sound.play()
    main_bgm.repeat_play()
    clear_in_out(e_x,e_y,o_x,o_y)

def death_check():
    if player.life == 0:
        main_bgm.stop()

    if player.death_time < 0:
        main_bgm.repeat_play()
        player.life = 5
        player.score = 0
        player.boom_count = 4
        player.rope_count = 4
        player.death_time = 8
        reset()

def ufo_maker():
    global ufo_count, stage_time
    if ufo_count < 1 and stage_time > 30:
        x = random.choice([-100,2680])
        y = 1200
        pos = x,y
        new_ufo = ufo.Ufo(pos)
        gfw.world.add(gfw.layer.ufo, new_ufo)
        ufo_count += 1
        main_bgm.stop()
        ufo_bgm.repeat_play()
    else:
        for u in gfw.world.objects_at(gfw.layer.ufo):
            u.find_me(player)

def fade_in_out():
    global black_canvas, black_pos
    b_x, b_y = black_pos
    if player.stage_clear == True:
        gfw.world.clear_at(gfw.layer.ufo)
        ufo_bgm.stop()
        main_bgm.stop()
        if b_y > 0:
            b_y -= 10
        else:
            reset()
    elif player.death_time < 8:
        if b_y > 0:
            b_y -= 4
    else:
        if b_y < get_canvas_height() + 600:
            b_y += 10
    black_pos = b_x, b_y

def clear_in_out(x1,y1,x2,y2):
    for t in gfw.world.objects_at(gfw.layer.tile):
        if t.left == x1 and t.bottom == y1 and t.name != 'entrance':
            gfw.world.remove(t)
        elif t.left == x2 and t.bottom == y2 and t.name != 'exit':
            gfw.world.remove(t)

def change_to_screen(x1,y1,x2,y2):
    x1 = x1 * 640 + 320
    y1 = y1 * 512 + 192
    x2 = x2 * 640 + 320
    y2 = y2 * 512 + 192
    return x1,y1,x2,y2

if __name__ == '__main__':
    gfw.run_main()
