import random
from pico2d import *
import gfw
import gobj
import effect

ufoimage = None

FULL_MAP_WIDTH = 2560
FULL_MAP_HEIGHT = 2048

def load():
    global ufoimage
    if ufoimage is None:
        ufoimage = gfw.image.load(gobj.res('ufo.png'))

class Ufo:
    Animation = [0x60,0x61,0x62,0x63,0x64,0x65]

    def __init__(self, pos):
        self.pos = pos
        self.draw_pos = self.pos
        self.dy = 0
        self.dx = 0
        self.speed = 50
    
        self.time = 0 
    
        self.mag = 2
    
        self.size = 300
        self.unit = 80
    
        self.fidx = 0
        self.FPS = 12

        self.anim = Ufo.Animation

    def update(self):
        x,y = self.pos
        x += self.dx * self.speed * self.mag * gfw.delta_time
        y += self.dy * self.speed * gfw.delta_time

        self.pos = x,y
        self.time += gfw.delta_time

        if self.time > 1:
            self.explosion()
            self.time = 0

        frame = self.time * self.FPS
        self.fidx = int(frame) % len(self.anim)
            
    def draw(self):
        x, y = self.draw_pos
        
        sprite_num = self.anim[self.fidx]

        sx, sy = sprite_num % 0x10, sprite_num // 0x10
        sx = sx * self.unit
        sy = sy * self.unit + 64

        ufoimage.clip_draw(sx, sy, self.unit, self.unit, *self.draw_pos, self.size,self.size)

    def explosion(self):
        boom_effect = effect.Explosion_effect(self.pos, self.size)
        gfw.world.add(gfw.layer.effect, boom_effect)
        boom_effect.explosion_sound1.set_volume(3)
        boom_effect.explosion_sound2.set_volume(3)
        boom_effect.explosion_sound1.play()
        boom_effect.explosion_sound2.play()

    def set_draw_pos(self, LEFT_GAB, BOTTOM_GAB):
        x, y = self.pos
        x = x - LEFT_GAB
        y = y - BOTTOM_GAB
        self.draw_pos = x,y

    def find_me(self, player):
        x,y = self.pos
        p_x, p_y = player.pos
        if x < p_x:
            self.dx = 1
        else:
            self.dx = -1
        if y < p_y:
            self.dy = 2
        else:
            self.dy = -2

    def get_bb(self):
        x,y = self.draw_pos
        return x - self.size // 2, y - self.size// 2 , x + self.size // 2, y + self.size // 2