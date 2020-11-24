import random
from pico2d import *
import gfw
import gobj
import tile

GRAVITY = 9

class Something:
    def __init__(self,pos,imageName):
        self.pos = pos
        self.draw_pos = self.pos
        self.dy = 0
        self.dx = 0
        self.image = gfw.image.load(imageName)
        self.time = 0 
        self.mag = 2     

    def update(self):
        tile = self.get_tile()
        wall = self.get_wall()

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

    def set_draw_pos(self, pos):
        self.draw_pos = pos

    def get_bb(self):
        hw = 24
        hh = 28
        x,y = self.draw_pos
        return x - hw, y - hh, x + hw, y + hh

    def get_tile(self):
        selected = None
        sel_top = 0
        _,foot,_,_ = self.get_bb()
        x,y = self.draw_pos
        for tile in gfw.world.objects_at(gfw.layer.tile):
            if tile.name == 'ledder_bottom': continue
            if tile.name in ['entrance', 'exit']: continue
            if tile.name == 'ledder_top': continue
            l,b,r,t = tile.get_bb()
            if x < l - 10 or x > r + 10: continue
            gab = (b + t) // 2 + 5
            if foot < gab: continue
            if selected is None:
                selected = tile
                sel_top = t
            else:
                if t > sel_top:
                    selected = tile
                    sel_top = t
        # if selected is not None:
        #     print(l,b,r,t, selected)
        return selected

    def tile_check(self, tile,foot):
        l,b,r,t = tile.get_bb()
        dy = 0
        if foot > t:
            self.dy -= GRAVITY * gfw.delta_time   # 중력 적용
        else:
            # print('falling', t, foot)
            if self.dy <= 0 and int(foot) < t:
                dy = t - foot
                self.dy = 0
                # print('Now running', t, foot)
        return dy

    def get_wall(self):
        selected = None
        _,y = self.draw_pos
        left,_,right,_ = self.get_bb()
        for tile in gfw.world.objects_at(gfw.layer.tile):
            if tile.name in ['entrance', 'exit','ledder_bottom','ledder_top']: continue
            l,b,r,t = tile.get_bb()
            if y > t or y < b: continue
            if right < l or left > r: continue
            selected = tile
        return selected

    def wall_check(self, wall,left, right):
        if wall is not None:
            l,b,r,t = wall.get_bb()
            if self.look_left is True and r > left and l < left:
                self.mag = 0
            elif self.look_left is not True and l < right and l > left:
                self.mag = 0
            else:
                self.mag = 2
        else:
            self.mag = 2