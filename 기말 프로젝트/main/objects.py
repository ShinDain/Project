import random
from pico2d import *
import gfw
import gobj
import effect
import tile

GRAVITY = 9

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
    def __init__(self,pos):
        self.pos = pos
        self.draw_pos = self.pos
        self.dy = 0.1
        self.dx = 0

        self.time = 0 
        self.mag = 2
        self.speed = 100

        self.grabed = False

        self.unit = 80
        self.remove_b = False
        self.remove_time = 1
        self.moving = True

        self.init()

    def init(self):
        self.name = 'box'
        self.rect = object_rects[self.name]
        self.collide_sound = load_wav('res/wav/crateopen.wav')
        self.moving = True

    def update(self):
        if self.dx != 0 and self.dy != 0:
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
        if self.time > 1:
            self.grabed = False
        else:
            self.grabed = True
        if self.remove_b == True:
            self.remove_time -= gfw.delta_time
        if self.remove_time < 0:
            self.remove()
            
    def draw(self):
        x, y = self.draw_pos
        if x < -64 or x > get_canvas_width() + 64: return
        if y < -64 or y > get_canvas_height() + 64: return

        objectimage.clip_draw(*self.rect, *self.draw_pos, self.unit, self.unit)

    def set_draw_pos(self, LEFT_GAB, BOTTOM_GAB):
        x, y = self.pos
        x = x - LEFT_GAB
        y = y - BOTTOM_GAB
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

        select = random.choice([Bomb_pack, Rope_pack, Stone])
        obj = select(self.pos)
        if select == Stone:
            gfw.world.add(gfw.layer.object, obj)
        else:
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

    def wall_check(self, wall,left,right):
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

class Treasure_box(Something):
    def init(self):
        self.name = 'treasure_box'
        self.rect = object_rects[self.name]
        self.collide_sound = load_wav('res/wav/chestopen.wav')
        self.moving = True

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
        select = random.choice([Money,Gold_top,Gem1,Gem2,Gem3,Gem4])
        obj = select(self.pos)
        gfw.world.add(gfw.layer.score_object, obj)

class Arrow(Something):
    def __init__(self,pos, look):
        self.pos = pos
        self.draw_pos = self.pos
        self.dy = 0
        self.dx = 0

        self.time = 0 
        self.mag = 2
        self.speed = 100

        self.grabed = False

        self.unit = 80
        self.look_left = look

        self.remove_b = False
        self.remove_time = 1
        self.moving = True
        self.init()

    def init(self):
        self.name = 'arrow'
        self.rect = object_rects[self.name]
        self.collide_sound = load_wav('res/wav/arrowhitwall.wav')
        self.moving = True

    def draw(self):
        x, y = self.draw_pos
        if x < -64 or x > get_canvas_width() + 64: return
        if y < -64 or y > get_canvas_height() + 64: return

        if self.look_left is False:
            objectimage.clip_draw(*self.rect, *self.draw_pos, self.unit, self.unit)
        else:
            objectimage.clip_composite_draw(*self.rect,0,'h', *self.draw_pos, self.unit, self.unit)

    def collide(self):
        if self.grabed == True:
            return False
        if self.dx > 2 or self.dx < -2: 
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
        return x - 30, y - 12, x + 30, y + 5

class Money(Something):
    def init(self):
        self.name = 'gold_bar'
        self.rect = object_rects[self.name]
        self.collide_sound = load_wav('res/wav/chime.wav')
        self.already = False
        self.score = 100

    def draw(self):
        x, y = self.draw_pos
        if x < -64 or x > get_canvas_width() + 64: return
        if y < -64 or y > get_canvas_height() + 64: return

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
        return x - 15, y - 10, x + 15, y + 10

class Gold_top(Money):
    def init(self):
        self.name = 'gold_top'
        self.rect = object_rects[self.name]
        self.collide_sound = load_wav('res/wav/chime3.wav')
        self.already = False
        self.score = 500

    def get_bb(self):
        x,y = self.draw_pos
        return x - 25, y - 10, x + 25, y + 12

class Gem1(Money):
    def init(self):
        self.name = 'gem1'
        self.rect = object_rects[self.name]
        self.collide_sound = load_wav('res/wav/gem1.wav')
        self.already = False
        self.score = 1000

    def get_bb(self):
        x,y = self.draw_pos
        return x - 15, y - 24, x + 15, y + 10

class Gem2(Gem1):
    def init(self):
        self.name = 'gem2'
        self.rect = object_rects[self.name]
        self.collide_sound = load_wav('res/wav/gem2.wav')
        self.already = False
        self.score = 2000

class Gem3(Gem1):
    def init(self):
        self.name = 'gem3'
        self.rect = object_rects[self.name]
        self.collide_sound = load_wav('res/wav/gem3.wav')
        self.already = False
        self.score = 3000

class Gem4(Gem1):
    def init(self):
        self.name = 'gem4'
        self.rect = object_rects[self.name]
        self.collide_sound = load_wav('res/wav/gem4.wav')
        self.already = False
        self.score = 5000

class Bomb_pack(Gold_top):
    def init(self):
        self.name = 'bomb_pack'
        self.rect = object_rects[self.name]
        self.collide_sound = load_wav('res/wav/collect.wav')
        self.already = False
        self.score = 3

    def get_bb(self):
        x,y = self.draw_pos
        return x - 15, y - 25, x + 15, y + 10

class Rope_pack(Gold_top):
    def init(self):
        self.name = 'rope_pack'
        self.rect = object_rects[self.name]
        self.collide_sound = load_wav('res/wav/collect.wav')
        self.already = False
        self.score = 3

    def get_bb(self):
        x,y = self.draw_pos
        return x - 15, y - 25, x + 15, y + 10

class Stone(Arrow):
    def __init__(self,pos):
        self.pos = pos
        self.draw_pos = self.pos
        self.dy = 0
        self.dx = 0

        self.time = 0 
        self.mag = 2
        self.speed = 100

        self.grabed = False

        self.unit = 80
        self.remove_b = False
        self.remove_time = 1

        self.moving = True

        self.init()

    def init(self):
        self.name = 'stone'
        self.rect = object_rects[self.name]
        self.collide_sound = load_wav('res/wav/item_drop.wav')

    def draw(self):
        x, y = self.draw_pos
        if x < -64 or x > get_canvas_width() + 64: return
        if y < -64 or y > get_canvas_height() + 64: return

        objectimage.clip_draw(*self.rect, *self.draw_pos, self.unit, self.unit)

    def get_bb(self):
        x,y = self.draw_pos
        return x - 10, y - 10, x + 10, y + 10

class Bomb(Something):
    def init(self):
        self.name = 'boom1'
        self.rect = object_rects[self.name]
        self.timer_sound = load_wav('res/wav/bomb_timer.wav')
        self.explosion_sound1 = load_wav('res/wav/kaboom.wav')
        self.explosion_sound2 = load_wav('res/wav/kaboombass.wav')

    def update(self):
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
        
        self.remove_time -= gfw.delta_time

        if self.remove_time < 0:
            self.explosion()
        elif self.remove_time < 2.5:
            if self.rect != object_rects['boom2']:
                self.rect = object_rects['boom2']
            else:
                self.rect = object_rects['boom3']

    def draw(self):
        x, y = self.draw_pos
        if x < -64 or x > get_canvas_width() + 64: return
        if y < -64 or y > get_canvas_height() + 64: return
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
        self.remove_time = 3
        boom_effect = effect.Explosion_effect(self.pos)
        gfw.world.add(gfw.layer.effect, boom_effect)
        boom_effect.explosion_sound1.set_volume(20)
        boom_effect.explosion_sound2.set_volume(20)
        boom_effect.explosion_sound1.play()
        boom_effect.explosion_sound2.play()
        self.remove()

class Rope(Something):
    def init(self):
        self.name = 'rope_object'
        self.rect = object_rects[self.name]

    def update(self):
        x,y = self.pos
        x += self.dx * self.speed * self.mag * gfw.delta_time
        y += self.dy * self.speed * gfw.delta_time
        
        self.dy -= GRAVITY * gfw.delta_time   # 중력 적용

        self.get_floor()

        x = clamp(20, x,FULL_MAP_WIDTH - 20)
        y = clamp(0, y,FULL_MAP_HEIGHT)

        self.make_rope()

        self.pos = x,y
        self.time += gfw.delta_time

    def make_rope(self):
        x,y = self.pos
        x -= 32
        y -= 32
        if self.dy <= 0:
            rope1 = tile.Rope_top('rope_top', x, y)
            rope2 = tile.Rope_mid('rope_mid', x, y - tile.BLOCK_SIZE)
            rope3 = tile.Rope_mid('rope_mid', x, y - tile.BLOCK_SIZE * 2)
            rope4 = tile.Rope_mid('rope_mid', x, y - tile.BLOCK_SIZE * 3)
            rope5 = tile.Rope_last('rope_last', x, y - tile.BLOCK_SIZE * 4)
            gfw.world.add(gfw.layer.tile, rope1)
            gfw.world.add(gfw.layer.tile, rope2)
            gfw.world.add(gfw.layer.tile, rope3)
            gfw.world.add(gfw.layer.tile, rope4)
            gfw.world.add(gfw.layer.tile, rope5)
            self.remove()
