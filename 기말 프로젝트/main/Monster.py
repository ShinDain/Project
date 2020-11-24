import random
from pico2d import *
import gfw
import gobj
import tile
from box import Something

GRAVITY = 9

class Monster(Something):
    def __init__(self,pos,name):
    self.pos = pos
    self.draw_pos = self.pos
    self.dy = 0
    self.dx = 0
    self.image = gfw.image.load(gobj.res('monster.png'))
    self.time = 0 
    self.mag = 2
    self.name = name

    def update(self):
    	tile = self.get_tile()
        wall = self.get_wall()
        self.get_floor()
        
        x,y = self.pos
        x += self.dx * self.speed * self.mag * gfw.delta_time
        y += self.dy * self.speed * gfw.delta_time
        
        dy = 0
        if tile is not None:
            dy = self.tile_check(tile,foot)
            y += dy
        else: 
            self.dy -= GRAVITY * gfw.delta_time   # 중력 적용

        x -= dx
        self.wall_check(wall,left,right)

        x = clamp(20, x,FULL_MAP_WIDTH - 20)
        y = clamp(0, y,FULL_MAP_HEIGHT)

        self.pos = x,y
        self.time += gfw.delta_time

    def get_floor(self):
        if self.dy == True and self.jump_time < 0.3:
            self.jump_speed = 1.5
            self.jump_time += gfw.delta_time
        else:
            self.jump_time = 0
            self.jump_on = False

        x, y = self.draw_pos
        _,_,_,P_top = self.get_bb()
        for tile in gfw.world.objects_at(gfw.layer.tile):
            if tile.name in ['entrance', 'exit']: continue
            if tile.name == 'ledder_bottom' or tile.name == 'ledder_top': continue
            l,b,r,t = tile.get_bb()
            if x > r + 10 or x < l - 10: continue
            gab = (b + t) // 2
            if y > gab: continue
            if P_top < b:
                pass
            else:
                if self.jump_speed > 0:
                    self.jump_speed = 0
                    self.jump_on = False
                    self.jump_time = 0