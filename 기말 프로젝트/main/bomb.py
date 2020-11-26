import random
from pico2d import *
import gfw
import gobj
import tile
from objects import Something

class Bomb(Something):
    def __init__(self,pos,name):
        self.pos = pos
        self.draw_pos = self.pos
        self.dy = 0
        self.dx = 0

        self.name = name
        self.rect = object_rects[name]

        self.time = 0 
        self.mag = 2
        self.speed = 100

        self.unit = 80
        self.left_gab = 0
        self.bottom_gab = 0

        self.remove_time = 0

        self.collide_sound = load_wav('res/wav/chestopen.wav')

    def update(self):
        tile = self.get_tile()
        wall = self.get_wall()

        x,y = self.pos
        x += self.dx * self.speed * self.mag * gfw.delta_time
        y += self.dy * self.speed * gfw.delta_time
        
        dy = 0
        if tile is not None:
            dy = self.tile_check(tile)
            y += dy
        else: 
            self.dy -= GRAVITY * gfw.delta_time   # 중력 적용

        self.wall_check(wall)
        self.get_floor()

        x = clamp(20, x,FULL_MAP_WIDTH - 20)
        y = clamp(0, y,FULL_MAP_HEIGHT)

        self.pos = x,y
        self.set_draw_pos()
        self.time += gfw.delta_time
        if self.remove_time > 0:
            self.remove_time -= gfw.delta_time
        elif self.remove_time < 0:
            self.remove()

    def draw(self):
        if self.already == True : return
        x, y = self.pos
        objectimage.clip_draw(*self.rect, *self.draw_pos, self.unit, self.unit)

    def collide(self):
        if self.already == True : return 0
        self.remove_time = 1
        self.collide_sound.play()
        self.already = True
        return self.score

    def collide_whip(self, pos):
        o_x, o_y = self.pos
        p_x, p_y = pos
        if o_x < p_x:
            self.change_dx(-1)
            self.change_dy(1)
        else:
            self.change_dx(1) 
            self.change_dy(1)

        self.collide_sound.play()
        self.time = 0

    def get_bb(self):
        x,y = self.draw_pos
        return x - 15, y - 24, x + 15, y + 10
