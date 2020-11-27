import random
from pico2d import *
import gfw
import gobj
import tile
import collision
import effect

GRAVITY = 5

objectimage = None
object_rects = {}

FULL_MAP_WIDTH = 2560
FULL_MAP_HEIGHT = 2048

def load():
    global objectimage
    if objectimage is None:
        objectimage = gfw.image.load(gobj.res('object.png'))
        with open(gobj.res('object.json')) as f:
            data = json.load(f)
            for name in data:
                object_rects[name] = tuple(data[name])

class Something:
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

        self.grabed = False

        self.unit = 80
        self.left_gab = 0
        self.bottom_gab = 0

        self.remove_b = False
        self.remove_time = 1

        if name == 'box':
            self.collide_sound = load_wav('res/wav/crateopen.wav')
        elif name == 'treasure_box':
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
        if self.remove_b == True:
            self.remove_time -= gfw.delta_time
        if self.remove_time < 0:
            self.remove()
            
    def draw(self):
        x, y = self.pos
        objectimage.clip_draw(*self.rect, *self.draw_pos, self.unit, self.unit)

    def set_draw_pos(self):
        x, y = self.pos
        x = x - self.left_gab
        y = y - self.bottom_gab
        self.draw_pos = x,y

    def set_pos(self, pos):
        self.pos = pos

    def get_bb(self):
        hw = 32
        hh = 32
        x,y = self.draw_pos
        return x - hw, y - 24, x + hw, y + hh

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
        self.remove_b = True

        if self.name == 'box':
            select = random.choice(['boom_pack', 'rope_pack', 'stone'])
            score = 0
            if select == 'boom_pack':
                score = 3
                obj = Money(self.pos,select, score)
                gfw.world.add(gfw.layer.score_object, obj)
            elif select == 'rope_pack':
                score = 3
                obj = Money(self.pos,select, score)
                gfw.world.add(gfw.layer.score_object, obj)
            elif select == 'stone':
                obj = Something(self.pos,select)
                gfw.world.add(gfw.layer.object, obj)
            
        elif self.name == 'treasure_box':
            select = random.choice(['gold_bar','gold_top','gem1','gem2','gem3','gem4'])
            score = 0
            if select == 'gold_bar':
                score = 100
            elif select == 'gold_top':
                score = 300
            elif select == 'gem1':
                score = 1000
            elif select == 'gem2':
                score = 2000
            elif select == 'gem3':
                score = 3000
            elif select == 'gem4':
                score = 5000
            obj = Money(self.pos,select, score)
            gfw.world.add(gfw.layer.score_object, obj)
            
    def collide(self):
        pass

    def collide_bomb(self):
        self.remove()

    def remove(self):
        gfw.world.remove(self)

    def change_dx(self, dx):
        self.dx = dx

    def change_dy(self, dy):
        self.dy = dy        

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
        if wall is not None:
            l,b,r,t = wall.get_bb()
            if self.dx < 0 and r > left and l < left:
                self.dx = -self.dx // 2
            elif self.dx > 0 and l < right and l > left:
                self.dx = -self.dx // 2 
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

class Arrow(Something):
    def __init__(self,pos,name, look):
        self.pos = pos
        self.draw_pos = self.pos
        self.dy = 0
        self.dx = 0

        self.name = name
        self.rect = (640,864,80,80)

        self.time = 0 
        self.mag = 2
        self.speed = 100

        self.unit = 80
        self.left_gab = 0
        self.bottom_gab = 0

        self.grabed = False

        self.look_left = look
        self.remove_b = False
        self.remove_time = 0

        self.collide_sound = load_wav('res/wav/arrowhitwall.wav')

    def draw(self):
        if self.look_left is False:
            objectimage.clip_draw(*self.rect, *self.draw_pos, self.unit, self.unit)
        else:
            objectimage.clip_composite_draw(*self.rect,0,'h', *self.draw_pos, self.unit, self.unit)

    def collide(self):
        if self.grabed == True:
                return False
        if self.dx > 2 or self.dx < -2  : 
            self.dx = -self.dx // 2
            return True
        else:
            return False
            
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
        self.time = 0.5

    def get_bb(self):
        x,y = self.draw_pos
        if self.look_left == False:
            return x - 30, y - 12, x + 30, y + 5
        else:
            return x - 30, y - 12, x + 30, y + 5

class Money(Something):
    def __init__(self,pos,name, score):
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

        self.grabed = False

        self.score = score

        self.already = False
        self.remove_b = False
        self.remove_time = 1

        if name == 'gold_bar':
            self.collide_sound = load_wav('res/wav/chime.wav')
        elif name == 'gold_top':
            self.collide_sound = load_wav('res/wav/chime3.wav')
        elif name == 'gem1':
            self.collide_sound = load_wav('res/wav/gem1.wav')
        elif name == 'gem2':
            self.collide_sound = load_wav('res/wav/gem2.wav')
        elif name == 'gem3':
            self.collide_sound = load_wav('res/wav/gem3.wav')
        elif name == 'gem4':
            self.collide_sound = load_wav('res/wav/gem4.wav')

    def draw(self):
        if self.already == True : return
        x, y = self.pos
        objectimage.clip_draw(*self.rect, *self.draw_pos, self.unit, self.unit)

    def collide(self):
        if self.already == True : return 0
        self.remove_b = True
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

        #self.collide_sound.play()
        self.time = 0

    def get_bb(self):
        x,y = self.draw_pos
        if self.name == 'gold_bar':
            return x - 12, y - 10, x + 12, y + 8
        elif self.name == 'gold_top':
            return x - 25, y - 10, x + 25, y + 12
        else:
            return x - 15, y - 24, x + 15, y + 10


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

        self.remove_time = 3

        self.timer_sound = load_wav('res/wav/bomb_timer.wav')
        self.explosion_sound1 = load_wav('res/wav/kaboom.wav')
        self.explosion_sound2 = load_wav('res/wav/kaboombass.wav')

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
        
        self.remove_time -= gfw.delta_time

        if self.remove_time < 0:
            self.explosion()

    def draw(self):
        x, y = self.pos
        objectimage.clip_draw(*self.rect, *self.draw_pos, self.unit, self.unit)

    def collide(self):
        pass

    def collide_whip(self, pos):
        o_x, o_y = self.pos
        p_x, p_y = pos
        if o_x < p_x:
            self.change_dx(-1)
            self.change_dy(1)
        else:
            self.change_dx(1) 
            self.change_dy(1)
        self.time = 0

    def collide_bomb(self):
        self.explosion()

    def get_bb(self):
        x,y = self.draw_pos
        return x - 15, y - 20, x + 15, y + 10

    def explosion(self):
        boom_effect = effect.Explosion_effect(self.pos)
        gfw.world.add(gfw.layer.effect, boom_effect)
        boom_effect.explosion_sound1.play()
        boom_effect.explosion_sound2.play()
        self.remove()