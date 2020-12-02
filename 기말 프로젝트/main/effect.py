import random
from pico2d import *
import gfw
import gobj
from collision import collide

GRAVITY = 9

class Explosion_effect:
    def __init__(self, pos, size):
        self.pos = pos
        self.draw_pos = 5000,5000
        self.image = gfw.image.load('res/explosion.png')

        self.time = 0

        self.index = 0
        self.fidx = 0
        self.fidy = 0
        self.unit = size

        self.explosion_sound1 = load_wav('res/wav/kaboom.wav')
        self.explosion_sound2 = load_wav('res/wav/kaboombass.wav')

    def update(self):
        self.active()
        self.time += gfw.delta_time

        self.index += 1
        self.fidx = self.index % 9
        self.fidy = self.index // 9

        if self.index == 74:
            self.remove()

    def draw(self):
        self.image.clip_draw(self.fidx * 92 + 2, 736 - self.fidy * 92,92,92, *self.draw_pos, self.unit, self.unit)

    def active(self):
        for t in gfw.world.objects_at(gfw.layer.tile):
            crash = False
            if t.excludes_remove: continue
            crash = collide(t,self)
            if crash == True:
                t.remove()
        for obj in gfw.world.objects_at(gfw.layer.object):
            crash = collide(obj,self)
            if crash == True:
                obj.remove()
        for m in gfw.world.objects_at(gfw.layer.monster):
            crash = collide(m,self)
            if crash == True:
                m.remove()
        for p in gfw.world.objects_at(gfw.layer.player):
            p_crash = collide(p, self)
            if p_crash == True:
                p.dameged_to_die()

    def set_draw_pos(self, LEFT_GAB, BOTTOM_GAB):
        x, y = self.pos
        x = x - LEFT_GAB
        y = y - BOTTOM_GAB
        self.draw_pos = x,y

    def remove(self):
        gfw.world.remove(self)

    def get_bb(self):
        if self.time > 0.1:
            return 50000,50000,50000,50000

        x,y = self.draw_pos
        return x - self.unit//2, y - self.unit//2, x + self.unit//2, y + self.unit//2

class Blood:
    def __init__(self, pos):
        self.pos = pos
        self.draw_pos = pos
        self.image = gfw.image.load('res/object.png')
        self.rect = (1440,944,80,80)

        self.speed = 100
        self.mag = 2

        self.dx = random.uniform(-2,2)
        self.dy = random.uniform(2,4)
        self.size = 32

        self.time = 0

        self.monster_die_sound = load_wav('res/wav/spike_hit.wav')
        self.remove_time = 0

        self.monster_die_sound.set_volume(10)
        self.monster_die_sound.play()

    def update(self):
        x,y = self.pos
        x += self.dx * self.speed * self.mag * gfw.delta_time
        y += self.dy * self.speed * gfw.delta_time
        
        self.pos = x,y
        self.time += gfw.delta_time
        self.remove_time += gfw.delta_time
        if self.remove_time > 2:
            self.remove()

        self.dy -= GRAVITY * gfw.delta_time   # 중력 적용

    def remove(self):
        gfw.world.remove(self)

    def draw(self):
        x, y = self.draw_pos
        if x < -64 or x > get_canvas_width() + 64: return
        if y < -64 or y > get_canvas_height() + 64: return
        
        self.image.clip_draw(*self.rect, *self.draw_pos, self.size,self.size)
        
    def set_draw_pos(self,LEFT_GAB,BOTTOM_GAB):
        x, y = self.pos
        x = x - LEFT_GAB
        y = y - BOTTOM_GAB
        self.draw_pos = x,y

    def get_bb(self):
        x,y = self.draw_pos
        return x - 3, y - 3, x + 3, y + 3