import random
from pico2d import *
import gfw
import gobj
from collision import collide

LEFT_GAB = 0
BOTTOM_GAB = 0

BLOCK_SIZE = 64

class Explosion_effect:
    def __init__(self, pos):
        self.pos = pos
        self.draw_pos = pos
        self.image = gfw.image.load('res/explosion.png')

        self.time = 0

        self.index = 0
        self.fidx = 0
        self.fidy = 0
        self.unit = 240

        self.explosion_sound1 = load_wav('res/wav/kaboom.wav')
        self.explosion_sound2 = load_wav('res/wav/kaboombass.wav')

    def update(self):
        self.active()
        self.time += gfw.delta_time

        self.index += 1
        self.fidx = self.index % 9
        self.fidy = self.index // 9

        self.set_draw_pos()

        if self.index == 74:
            self.remove()

    def draw(self):
        self.image.clip_draw(self.fidx * 92 + 2, 736 - self.fidy * 92,92,92, *self.draw_pos, self.unit, self.unit)

    def active(self):
        crash = False
        for t in gfw.world.objects_at(gfw.layer.tile):
            if t.name in ['exit', 'entrance','cant_break']:continue
            crash = collide(t,self)
            if crash == True:
                t.remove()
        for obj in gfw.world.objects_at(gfw.layer.object):
            if obj == self : continue
            crash = collide(obj,self)
            if crash == True:
                obj.collide_bomb()
        for m in gfw.world.objects_at(gfw.layer.monster):
            if m == self : continue
            crash = collide(m,self)
            if crash == True:
                m.collide_whip((0,0))
        for p in gfw.world.objects_at(gfw.layer.player):
            p_crash = collide(p, self)
            if p_crash == True:
                p.dameged_to_die()

    def set_draw_pos(self):
        x, y = self.pos
        x = x - LEFT_GAB
        y = y - BOTTOM_GAB
        self.draw_pos = x,y

    def remove(self):
        gfw.world.remove(self)

    def get_bb(self):
        if self.time > 0.1:
            return 0,0,0,0

        x,y = self.draw_pos
        return x - BLOCK_SIZE * 1.5, y - BLOCK_SIZE * 1.5, x + BLOCK_SIZE * 1.5, y + BLOCK_SIZE * 1.5