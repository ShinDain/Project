import random
from pico2d import *
import gfw
import gobj
import tile

class Player:
    KEY_MAP = {
        (SDL_KEYDOWN, SDLK_LEFT):  (-1,  0),
        (SDL_KEYDOWN, SDLK_RIGHT): ( 1,  0),
        (SDL_KEYDOWN, SDLK_DOWN):  ( 0, -1),
        (SDL_KEYDOWN, SDLK_UP):    ( 0,  1),
        (SDL_KEYUP, SDLK_LEFT):    ( 1,  0),
        (SDL_KEYUP, SDLK_RIGHT):   (-1,  0),
        (SDL_KEYUP, SDLK_DOWN):    ( 0,  1),
        (SDL_KEYUP, SDLK_UP):      ( 0, -1),
    }
    KEYDOWN_SPACE  = (SDL_KEYDOWN, SDLK_SPACE)
    KEYUP_SPACE  = (SDL_KEYUP, SDLK_SPACE)
    KEYDOWN_LSHIFT = (SDL_KEYDOWN, SDLK_LSHIFT)
    KEYUP_LSHIFT   = (SDL_KEYUP,   SDLK_LSHIFT)
    image = None

    Animation = [
    [0xB0], # 기본
    [0xB1,0xB2,0xB3,0xB4,0xB5,0xB6,0xB7,0xB8], # 좌우로 이동
    [0xA0,0xA1,0xA2], # 엎드리기 
    [0xA2,0xA3,0xA4], # 일어서기
    [0xA5,0xA6,0xA7,0xA8,0xA9,0xAA,0xAB], # 기어서 이동
    [0x90,0x91,0x92,0x93], # 피격중
    [0xB9], # 기절, 사망
    [0x88,0x89,0x8A,0xB8], # 벽잡기
    [0x70,0x71,0x72,0x73,0x74,0x75], # 공격(채찍질)
    [0x76,0x77,0x78,0x79,0x7A], # 던지기
    [0x30,0x31,0x32,0x33,0x34,0x35,0x36], # 올려다보기
    [0x20,0x21,0x22,0x23,0x24,0x25], # 점프 
    [0x26,0x27,0x28,0x29,0x2A,0x2B], # 낙하
    [0x56,0x57,0x58,0x59,0x5A,0x5B], # 밀기
    [0x40,0x41,0x42,0x43,0x44,0x45,0x46,0x47,0x48,0x49], # 로프 타기
    [0x60,0x61,0x62,0x63,0x64,0x65], # 퇴장
    [0x66,0x67,0x68,0x69,0x6A,0x6B] # 입장
    ]

    IDLE, MOVE, CROUCH, STANDUP, CROUCH_MOVE, DAMAGED, \
    STUN_DEATH, GRAB_WALL, ATTACK, THROW, LOOKUP, JUMP, \
    FALLING, PUSHING, ROPE_MOVE, OUT_STAGE, IN_STAGE = range(17)

    Gravity = 7

    #constructor
    def __init__(self):
        self.pos = 240,360
        self.dx = 0
        self.jump_speed = 0
        self.jumpon = False
        self.jump_time = 0
        self.speed = 200
        self.image = gfw.image.load(gobj.RES_DIR + '/Player.png')
        self.time = 0
        self.mag = 2
        self.FPS = 20
        self.state = Player.IDLE;
        self.size = 80
        self.look_left = False;
        
    @property
    def state(self):
        return self.__state
    @state.setter
    def state(self, state):
        self.__state = state
        self.anim = Player.Animation[state]
    def draw(self):
        fidx = round(self.time * self.FPS) % len(self.anim)
        if self.state in [Player.LOOKUP,Player.CROUCH, Player.FALLING]:
            fidx = len(self.anim) - 1

        print(fidx)
        sprite_num = self.anim[fidx]

        sx, sy = sprite_num % 0x10, sprite_num // 0x10
        sx = sx * self.size
        sy = sy * self.size + 64

        if self.look_left is False:
            self.image.clip_draw(sx, sy, self.size, self.size, *self.pos, 80,80)
        else:
            self.image.clip_composite_draw(sx, sy, self.size, self.size, 0 , 'h', *self.pos , 80,80)

    def move(self):
        if self.state is not Player.IDLE: return
        elif self.state is Player.CROUCH:
            self.state = Player.CROUCH_MOVE
        else:
            self.state = Player.MOVE

    def jump(self):
        if self.state == Player.FALLING: return
        if self.state in [Player.IDLE,Player.MOVE]:
            self.state = Player.JUMP
        else:
            pass
    def update(self):
        left,foot,right,_ = self.get_bb()                      # 바닥 체크
        tile = self.get_tile(foot)
        wall = self.get_wall(left,right)
        self.get_floor()
        
        x,y = self.pos
        x += self.dx * self.speed * self.mag * gfw.delta_time
        y += self.jump_speed * self.speed * gfw.delta_time
        
        if self.state in [Player.FALLING, Player.JUMP]:
            self.jump_speed -= Player.Gravity * gfw.delta_time   # 중력 적용
        
        dy = 0
        if tile is not None:
            dy = self.tile_check(tile,foot)
            y += dy

        self.wall_check(wall,left,right)

        if self.state in [Player.FALLING, Player.JUMP]:
            self.FPS = 10
        self.pos = x,y
        self.time += gfw.delta_time

        if self.dx is 0 and self.jump_speed is 0:
            self.state = Player.IDLE

    def get_floor(self):
        if(self.jumpon == True and self.jump_time < 0.3):
            self.jump_speed = 1.5
            self.jump_time += gfw.delta_time
        else:
            self.jump_time = 0
            self.jumpon = False

        x, y = self.pos
        for tile in gfw.world.objects_at(gfw.layer.tile):
            l,b,r,t = tile.get_bb()
            if x > r or x < l: continue
            gab = (b + t) // 2
            if y > gab: continue
            if y + 20 < b:
                pass
            else:
                if self.jump_speed > 0:
                    self.jump_speed = 0
                    self.jumpon = False
                    self.jump_time = 0

    def get_tile(self, foot):
        selected = None
        sel_top = 0
        x,y = self.pos
        for tile in gfw.world.objects_at(gfw.layer.tile):
            l,b,r,t = tile.get_bb()
            if x < l or x > r: continue
            gab = (b + t) // 2 + 10
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
            if self.jump_speed > 0:
                self.state = Player.JUMP
            else:
                self.state = Player.FALLING
        else:
            # print('falling', t, foot)
            if self.jump_speed <= 0 and int(foot) < t:
                dy = t - foot
                self.state = Player.MOVE
                self.jump_speed = 0
                # print('Now running', t, foot)
        return dy

    def get_wall(self, left, right):
        selected = None
        _,y = self.pos
        for tile in gfw.world.objects_at(gfw.layer.tile):
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

    def handle_event(self, e):
        pair = (e.type, e.key)
        if pair in Player.KEY_MAP:
            self.dx += Player.KEY_MAP[pair][0]
            if self.dx is -1:
                self.look_left = True
                self.move()
            elif self.dx is 1:
                self.look_left = False
                self.move()
        # print(dx, pdx, self.action)
        elif pair == Player.KEYDOWN_SPACE:
            self.jump()
            if(self.state != Player.FALLING):
                self.jumpon = True
        elif pair == Player.KEYUP_SPACE:
            self.jumpon = False

    def get_bb(self):
        hw = 24
        hh = 28
        x,y = self.pos
        return x - hw, y - hh, x + hw, y + hh
