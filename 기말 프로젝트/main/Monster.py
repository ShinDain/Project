import random
from pico2d import *
import gfw
import gobj
import tile
import objects

GRAVITY = 5

monsterimage = None

FULL_MAP_WIDTH = 2560
FULL_MAP_HEIGHT = 2048

def load():
    global monsterimage
    if monsterimage is None:
        monsterimage = gfw.image.load(gobj.res('monster.png'))

class Monster(objects.Something):
    Animation = [
    [0xB0], # 기본
    [0xB0,0xB1,0xB2,0xB3,0xB4,0xB5,0xB6,0xB7,0xB8,0xB9,0xBA], # 이동 
    [0xA0,0xA1,0xA2,0xA3,0xA4,0xA5,0xA6] # 공격
    ]

    IDLE, MOVE, ATTACK = range(3)

    def __init__(self,pos,name):
        self.pos = pos
        self.draw_pos = self.pos
        self.dy = 0
        self.dx = 0
        self.speed = 10
    
        self.time = 0 
        self.state_time = 0
    
        self.mag = 2
        self.name = name
    
        self.size = 80
    
        self.fidx = 0
        self.FPS = 12
        self.state = Monster.IDLE
        self.look_left = False

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

        self.change_state()
        self.snake_move()

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
        self.state_time += gfw.delta_time

        if self.state in [Monster.ATTACK] and self.fidx >= len(self.anim) - 1:
            self.time = 0
            self.fidx = 0
            self.state = Monster.IDLE
        frame = self.time * self.FPS
        self.fidx = int(frame) % len(self.anim)
            
    def draw(self):
        x, y = self.draw_pos
        if x < -64 or x > get_canvas_width() + 64: return
        if y < -64 or y > get_canvas_height() + 64: return
        
        sprite_num = self.anim[self.fidx]

        sx, sy = sprite_num % 0x10, sprite_num // 0x10
        sx = sx * self.size + 5
        sy = sy * self.size + 64

        if self.look_left is False:
            monsterimage.clip_draw(sx, sy, self.size, self.size, *self.draw_pos, self.size,self.size)
        else:
            monsterimage.clip_composite_draw(sx, sy, self.size, self.size, 0 , 'h', *self.draw_pos, self.size,self.size)

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

    def snake_move(self):
        if self.state == Monster.MOVE:
            if self.look_left == True:
                self.dx = -1
            else:
                self.dx = 1
        else:
            self.dx = 0

    def change_state(self):
        if self.state_time > 3:
            state = random.choice([Monster.MOVE, Monster.IDLE])
            self.state = state
            self.look_left = random.choice([True,False])
            self.state_time = 0

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
            gab = (b + t) // 2 + 20
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

    def tile_check(self, tile):
        _,foot,_,_ = self.get_bb()
        l,b,r,t = tile.get_bb()
        dy = 0
        if foot > t:
            self.dy -= GRAVITY * gfw.delta_time   # 중력 적용
        else:
            # print('falling', t, foot)
            if self.dy <= 0 and int(foot) < t:
                dy = t - foot
                self.dy = 0
                self.dx = 0
                self.grabed = False
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

    def wall_check(self, wall):
        left,_,right,_ = self.get_bb()
        if wall is not None and self.state == Monster.MOVE:
            l,b,r,t = wall.get_bb()
            if self.dx < 0 and r > left and l < left:
                self.look_left = False
            elif self.dx > 0 and l < right and l > left:
                self.look_left = True
            else:
                self.mag = 2
        else:
            self.mag = 2

    def get_floor(self):
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
                if self.dy > 0:
                    self.dy = 0
