import gfw
from player import Player
from pico2d import *
import gobj
import stage_gen
import all_stage_gen

canvas_width = 1000
canvas_height = 800

def enter():
    gfw.world.init(['bg','tile','player'])
    global player
    player = Player()
    gfw.world.add(gfw.layer.player, player)

    bg = gobj.ImageObject('kpu_1280x960.png', (canvas_width // 2, canvas_height // 2))
    gfw.world.add(gfw.layer.bg, bg)

    all_stage_gen.make_all_map()

def update():
    gfw.world.update()
    
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
            for tile in gfw.world.objects_at(gfw.layer.tile):
                gfw.world.remove(tile)
            stage_gen.load(gobj.res('stages/stage_type0.txt'))
            stage_gen.update()
    player.handle_event(e)

def exit():
    pass

if __name__ == '__main__':
    gfw.run_main()
