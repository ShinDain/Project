import random
from pico2d import *
import gfw
import gobj
import tile
import objects
import effect

GRAVITY = 9

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

    def __init__(self,pos):
        self.pos = pos
        self.draw_pos = self.pos
        self.dy = 0
        self.dx = 0
        self.speed = 10
    
        self.time = 0 
        self.state_time = 0
    
        self.mag = 2
    
        self.size = 80
    
        self.fidx = 0
        self.FPS = 12
        self.state = Monster.IDLE
        self.look_left = False

        self.moving = True

    @property
    def state(self):
        return self.__state
    @state.setter
    def state(self, state):
        self.__state = state
        self.anim = Monster.Animation[state]

    def update(self):
        if self.dx != 0 or self.dy != 0:
            self.moving = True

        if self.moving:
            tile = self.get_tile()
            wall = self.get_wall()
    
            left,foot,right,_ = self.get_bb()
    
            x,y = self.pos
            move_x = self.dx * self.speed * self.mag * gfw.delta_time
            move_y = self.dy * self.speed * gfw.delta_time
            x += move_x
            y += move_y
    
            dy = 0
            if tile is not None:
                dy = self.tile_check(tile,foot + move_y)
                y += dy
                if dy > 0:
                    self.moving = False
            else: 
                self.dy -= GRAVITY * gfw.delta_time   # 중력 적용
    
            self.wall_check(wall,left + move_x,right + move_x)
            self.get_floor()
    
            x = clamp(20, x,FULL_MAP_WIDTH - 20)
            y = clamp(0, y,FULL_MAP_HEIGHT)
    
            self.pos = x,y

        self.time += gfw.delta_time
        self.state_time += gfw.delta_time

        self.change_state()
        self.snake_move()

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

    def dameged(self):
        for i in range(3):
            blood = effect.Blood(self.pos)
            gfw.world.add(gfw.layer.effect, blood)
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
            if tile.excludes_block: continue
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

    def tile_check(self, tile, foot):
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
            if tile.excludes_wall: continue
            l,b,r,t = tile.get_bb()
            if y > t or y < b: continue
            if right < l or left > r: continue
            selected = tile
        return selected

    def wall_check(self, wall, left, right):
        if wall is not None:
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
            if tile.excludes_floor: continue
            l,b,r,t = tile.get_bb()
            if x > r + 10 or x < l - 10: continue
            gab = (b + t) // 2
            if y > gab: continue
            if P_top < b:
                pass
            else:
                if self.dy > 0:
                    self.dy = 0

class Spider(Monster):
    Animation = [
    [0x95,0x96,0x97,0x98,0x99], # 기본
    [0xA7,0xA8,0xA9,0xAA] # 이동 
    ]

    IDLE, MOVE = range(2)

    def __init__(self,pos):
        self.pos = pos
        self.draw_pos = self.pos
        self.dy = 0
        self.dx = 0
        self.speed = 100
    
        self.time = 0 
        self.state_time = 0
    
        self.mag = 2
    
        self.size = 80
    
        self.fidx = 0
        self.FPS = 10
        self.state = Spider.IDLE

        self.moving = True

    @property
    def state(self):
        return self.__state
    @state.setter
    def state(self, state):
        self.__state = state
        self.anim = Spider.Animation[state]

    def update(self):
        if self.dx != 0 or self.dy != 0:
            self.moving = True

        if self.moving:
            tile = self.get_tile()
            wall = self.get_wall()
    
            left,foot,right,_ = self.get_bb()
    
            x,y = self.pos
            move_x = self.dx * self.speed * self.mag * gfw.delta_time
            move_y = self.dy * self.speed * gfw.delta_time
            x += move_x
            y += move_y
    
            dy = 0
            if tile is not None:
                dy = self.tile_check(tile,foot + move_y)
                y += dy
                if dy > 0:
                    self.moving = False
            else: 
                self.dy -= GRAVITY * gfw.delta_time   # 중력 적용
    
            self.wall_check(wall,left + move_x,right + move_x)
            self.get_floor()
    
            x = clamp(20, x,FULL_MAP_WIDTH - 20)
            y = clamp(0, y,FULL_MAP_HEIGHT)
    
            self.pos = x,y

        self.time += gfw.delta_time
        self.state_time += gfw.delta_time

        self.change_state()

        if self.state in [Spider.MOVE] and self.fidx >= len(self.anim) - 1:
            self.time = 0
            self.fidx = 0

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

        monsterimage.clip_draw(sx, sy, self.size, self.size, *self.draw_pos, self.size,self.size)

    def collide(self):
        pass

    def get_bb(self):
        x,y = self.draw_pos
        hw = 22
        hh = 20
        return x - hw, y - hh, x + hw, y + hh

    def change_state(self):
        d_x,_ = self.draw_pos

        if self.state_time > 2:
            state = random.choice([Spider.MOVE, Spider.IDLE])
            if state == Spider.MOVE:
                self.dy += 5
                self.dx += random.randint(-2,2)
            self.state = state
            self.look_left = random.choice([True,False])
            self.state_time = 0

    def tile_check(self, tile, foot):
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
                self.state = Spider.IDLE
                # print('Now running', t, foot)
        return dy

    def wall_check(self, wall, left, right):
        if wall is not None:
            l,b,r,t = wall.get_bb()
            if self.dx < 0 and r > left and l < left:
                self.dx = -self.dx
            elif self.dx > 0 and l < right and l > left:
                self.dx = -self.dx
            else:
                self.mag = 2
        else:
            self.mag = 2