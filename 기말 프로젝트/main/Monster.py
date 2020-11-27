import random
from pico2d import *
import gfw
import gobj
import tile
from objects import Something

GRAVITY = 5

monsterimage = None
monster_rects = {}

FULL_MAP_WIDTH = 2560
FULL_MAP_HEIGHT = 2048

class Monster(Something):
    Animation = [
    [0xB0], # 기본
    [0xB0,0xB1,0xB2,0xB3,0xB4,0xB5,0xB6,0xB7,0xB8,0xB9,0xBA], # 이동 
    [0xA0,0xA1,0xA2,0xA3,0xA4,0xA5,0xA6] # 공격
    ]

    IDLE, MOVE, ATTACK = range(3)

    def __init__(self,pos,name):
        self.pos = pos
        self.draw_pos = self.pos
        self.image = gfw.image.load(gobj.res('monster.png'))
        self.dy = 0
        self.dx = 0
        self.speed = 10
    
        self.time = 0 
    
        self.mag = 2
        self.name = name
    
        self.size = 80
    
        self.fidx = 0
        self.FPS = 12
        self.state = Monster.ATTACK
        self.look_left = False

        self.left_gab = 0
        self.bottom_gab = 0

    @property
    def state(self):
        return self.__state
    @state.setter
    def state(self, state):
        self.__state = state
        self.anim = Monster.Animation[state]

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

        frame = self.time * self.FPS
        self.fidx = int(frame) % len(self.anim)
            
    def draw(self):
        sprite_num = self.anim[self.fidx]

        sx, sy = sprite_num % 0x10, sprite_num // 0x10
        sx = sx * self.size + 5
        sy = sy * self.size + 64

        if self.look_left is False:
            self.image.clip_draw(sx, sy, self.size, self.size, *self.draw_pos, self.size,self.size)
        else:
            self.image.clip_composite_draw(sx, sy, self.size, self.size, 0 , 'h', *self.draw_pos, self.size,self.size)

    def collide(self):
        self.state = Monster.ATTACK
        self.fidx = 0
        self.time = 0

    def collide_whip(self, pos):
        self.remove()

    def get_bb(self):
        x,y = self.draw_pos
        hw = 22
        hh = 22
        return x - hw, y - hh, x + hw, y + hh
