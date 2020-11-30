from pico2d import *
import gfw
import gobj
import whip
import collision
import objects

FULL_MAP_WIDTH = 2560
FULL_MAP_HEIGHT = 2048

GRAVITY = 9

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
    KEYDOWN_Z = (SDL_KEYDOWN, SDLK_z)
    KEYUP_Z = (SDL_KEYUP, SDLK_z)
    KEYDOWN_X = (SDL_KEYDOWN, SDLK_x)
    
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
    [0x88,0x89,0x8A,0x8B], # 벽잡기
    [0x70,0x71,0x72,0x73,0x74,0x75], # 공격(채찍질)
    [0x76,0x77,0x78,0x79,0x7A], # 던지기
    [0x30,0x31,0x32,0x33], # 올려다보기
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

    #constructor
    def __init__(self,pos):
        self.dx = 0
        self.crouch = 0
        self.speed = 200
        self.image = gfw.image.load(gobj.res('Player.png'))        
        self.life = 4
        self.boom_count = 4
        self.rope_count = 4
        self.death_time = 8
        self.init(pos)
        
        self.hit_sound = load_wav('res/wav/hit.wav')
        self.jump_sound = load_wav('res/wav/jump.wav')
        self.land_sound = load_wav('res/wav/land.wav')
        self.death_sound = load_wav('res/wav/death.wav')
        self.spike_sound = load_wav('res/wav/spike_hit.wav')
        self.throw_sound = load_wav('res/wav/throw_item.wav')
        self.grab_sound = load_wav('res/wav/pickup.wav')

        self.set_volume()

    def init(self,pos):
        self.pos = pos
        self.draw_pos = self.pos
        
        self.jump_on = False
        self.jump_time = 0
        self.jump_speed = 0

        self.rope_on = False
        self.time = 0

        self.mag = 2
        self.FPS = 10
        
        self.size = 80
        self.look_left = False

        self.state = Player.IDLE
        self.fidx = 0

        self.dameged = False
        self.dameged_time = 0
        self.stun = False

        self.grab_item = None

        self.wall_grab = False
        self.attack = False
        self.throwing = False

        self.score = 0

        self.stage_clear = False
        

    @property
    def state(self):
        return self.__state
    @state.setter
    def state(self, state):
        self.__state = state
        self.anim = Player.Animation[state]
    def draw(self):
        sprite_num = self.anim[self.fidx]

        sx, sy = sprite_num % 0x10, sprite_num // 0x10
        sx = sx * self.size
        sy = sy * self.size + 64

        if self.look_left is False:
            self.image.clip_draw(sx, sy, self.size, self.size, *self.draw_pos, self.size,self.size)
        else:
            self.image.clip_composite_draw(sx, sy, self.size, self.size, 0 , 'h', *self.draw_pos, self.size,self.size)

    def update(self):
        if self.life == 0:
            if self.death_time == 8:
                self.death_sound.play()
                self.death_time -= gfw.delta_time
            else:
                self.death_time -= gfw.delta_time

        left,foot,right,_ = self.get_bb()           # 바닥 체크
        tile = self.get_tile(foot)
        wall = self.get_wall(left,right)

        dx = 0
        ledder = None
        if self.state in [Player.DAMAGED]:
            pass
        else:    
            dx, ledder = self.get_ledder()

        self.get_floor()

        x,y = self.pos
        if self.state in [Player.ROPE_MOVE,Player.LOOKUP, Player.DAMAGED, Player.STUN_DEATH, Player.GRAB_WALL]:
            pass
        else:
            x += self.dx * self.speed * self.mag * gfw.delta_time
        y += self.jump_speed * self.speed * gfw.delta_time
        
        dy = 0
        if tile is not None:
            dy = self.tile_check(tile,foot)
            y += dy
            if dy > 1:
                self.land_sound.play()
        else: 
            self.state = Player.FALLING
            self.jump_speed -= GRAVITY * gfw.delta_time   # 중력 적용
        if ledder is None:
            self.rope_on = False

        x -= dx
        self.wall_check(wall,left,right)

        x = clamp(20, x,FULL_MAP_WIDTH - 20)
        y = clamp(0, y,FULL_MAP_HEIGHT)

        self.pos = x,y
        self.time += gfw.delta_time
        self.dameged_time -= gfw.delta_time

        if self.grab_item is not None:
            tmpx,tmpy = self.pos
            if self.look_left == True:
                self.grab_item.look_left = True
                tmpx -= 20
            else:
                self.grab_item.look_left = False
                tmpx += 20
            pos = tmpx, tmpy
            self.grab_item.change_dy(0)
            self.grab_item.set_pos(pos)

        self.state_check()

        if self.state in [Player.LOOKUP,Player.CROUCH, Player.FALLING, Player.JUMP, Player.GRAB_WALL] and self.fidx == len(self.anim) - 1:
            self.fidx = len(self.anim) - 1
        elif self.state in [Player.DAMAGED] and self.fidx >= len(self.anim) - 1:
            self.stun = True
            self.time = 0
            self.fidx = 0
        elif self.state in [Player.ATTACK] and self.fidx >= len(self.anim) - 1:
            self.attack = False
            self.time = 0
            self.fidx = 0
            self.state = Player.IDLE
        elif self.state in [Player.THROW] and self.fidx >= len(self.anim) - 1:
            self.throwing = False
            self.time = 0
            self.fidx = 0
            self.state = Player.IDLE
        else:
            frame = self.time * self.FPS
            self.fidx = int(frame) % len(self.anim)

        if self.grab_item != None:
            self.grab_item.time = 0

        self.change_FPS()
        self.change_speed()
        # self.player.pos = point_add(self.player.pos, self.player.delta)

    def handle_event(self, e):
        pair = (e.type, e.key)
        if pair in Player.KEY_MAP:
            if self.state in [Player.DAMAGED, Player.STUN_DEATH, Player.ATTACK, Player.THROW]: pass
            else:
                self.time = 0
            if self.state is Player.CROUCH_MOVE:
                self.fidx = 2
            self.dx += Player.KEY_MAP[pair][0]
            self.crouch += Player.KEY_MAP[pair][1]
        if e.type == SDL_KEYDOWN:
            if e.key == SDLK_l:
                self.dameged_just()
            elif e.key == SDLK_k:
                self.dameged_to_stun()
            elif e.key == SDLK_a:
                self.use_rope()
            elif e.key == SDLK_s:
                self.use_bomb()

        if self.state in [Player.STUN_DEATH]: return
        if pair == Player.KEYDOWN_Z:
            self.wall_grab = False
            self.rope_on = False 
            self.jump()
        elif pair == Player.KEYUP_Z:
            self.jump_on = False
        elif pair == Player.KEYDOWN_X:
            self.use()
        elif pair == Player.KEYDOWN_SPACE:
            self.clear_check()

    def state_check(self):
        if self.stage_clear == True:
            self.state = Player.OUT_STAGE
            return

        if self.life == 0:
            self.state = Player.STUN_DEATH
            self.wall_grab = False
            return
        if self.dameged == True:
            if self.stun == True:
                self.state = Player.STUN_DEATH
            else:
                self.state = Player.DAMAGED
                self.wall_grab = False
            self.recover()
            return

        if self.attack == True:
            self.state = Player.ATTACK
            return

        if self.wall_grab == True:
            self.state = Player.GRAB_WALL
            return

        if self.throwing == True:
            self.state = Player.THROW
            return

        if self.dx is 0 and self.jump_speed is 0:
            if self.crouch is 1:
                self.state = Player.LOOKUP
            elif self.crouch is -1:
                self.state = Player.CROUCH
            else:
                self.state = Player.IDLE
        if self.dx is -1:
                self.look_left = True
                self.move()
        elif self.dx is 1:
                self.look_left = False
                self.move()
        if self.rope_on is True:
            self.state = Player.ROPE_MOVE

    def clear_check(self):
        x,y = self.draw_pos
        for t in gfw.world.objects_at(gfw.layer.tile):
            if t.name is not 'exit': continue
            l,b,r,t = t.get_bb()
            if x > r or x < l : continue
            if y > t or y < b : continue
            
            self.stage_clear = True

    def change_FPS(self):
        if self.state in [Player.MOVE]:
            self.FPS = 20
        elif self.state in [Player.LOOKUP, Player.CROUCH]:
            self.FPS = 10
        elif self.state in [Player.ATTACK]:
            self.FPS = 12
        else:
            self.FPS = 10

    def change_speed(self):
        if self.state in [Player.CROUCH_MOVE, Player.CROUCH]:
            self.speed = 50
        else:
            self.speed = 200

    def set_volume(self):
        self.hit_sound.set_volume(20)
        self.death_sound.set_volume(10)
        self.jump_sound.set_volume(15)
        self.land_sound.set_volume(15)
        self.spike_sound.set_volume(20)
        self.throw_sound.set_volume(15)
        self.grab_sound.set_volume(15)

    def set_draw_pos(self, pos):
        self.draw_pos = pos

    def get_bb(self):
        if self.state in [Player.CROUCH, Player.CROUCH_MOVE, Player.STUN_DEATH]:
            hw = 24
            hh = 28
            x,y = self.draw_pos
            return x - hw, y - hh, x + hw, y

        hw = 24
        hh = 28
        x,y = self.draw_pos
        return x - hw, y - hh, x + hw, y + hh

    def use_bomb(self):
        if self.boom_count == 0: return
        self.boom_count -= 1
        bomb = objects.Bomb(self.pos)
        gfw.world.add(gfw.layer.object,bomb)
        dx, dy = 0,0
        
        if self.crouch == 1:
            if self.look_left == True:
                dx -= 4
            else:
                dx += 4
            dy += 5
        elif self.crouch == -1:
            if self.look_left == True:
                dx -= 2
            else:
                dx += 2
            dy += 0.2
        else:
            if self.look_left == True:
                dx -= 4
            else:
                dx += 4
            dy += 1
            
        bomb.change_dx(dx)
        bomb.change_dy(dy)

        self.time = 0
        self.fidx = 0
        self.throwing = True
        self.throw_sound.play()

    def use_rope(self):
        if self.rope_count == 0: return
        self.rope_count -= 1
        
        x,y = self.pos
        x = (x // 64) * 64 + 32
        y = (y // 64) * 64 + 32
        dy = 0

        if self.crouch == -1:
            if self.look_left == True:
                x -= 64
            else:
                x += 64
            dy += 0
        else:
            y += 64
            dy += 7

        pos = x,y
        rope = objects.Rope(pos)

        rope.change_dy(dy)
        gfw.world.add(gfw.layer.object,rope)

    def grab(self):
        x,_ = self.draw_pos
        p_l,p_b,p_r,p_t = self.get_bb()
        for obj in gfw.world.objects_at(gfw.layer.object):
            crash = collision.collide(self,obj)
            if crash == True:
                self.grab_item = obj
                self.grab_sound.play()
                return True

    def throw(self):
        dx, dy = 0,0
        
        if self.crouch == 1:
            if self.look_left == True:
                dx -= 4
            else:
                dx += 4
            dy += 5
        elif self.crouch == -1:
            if self.look_left == True:
                dx -= 2
            else:
                dx += 2
            dy += 0.2
        else:
            if self.look_left == True:
                dx -= 4
            else:
                dx += 4
            dy += 1
            
        self.grab_item.change_dx(dx)
        self.grab_item.change_dy(dy)

        self.grab_item = None
        self.time = 0
        self.fidx = 0
        self.throwing = True
        self.throw_sound.play()

    def use(self):
        if self.grab_item is not None: 
            self.throw()
            return

        some = False
        if self.crouch == -1:
            some = self.grab()
        if some == True: return
        if self.attack == True : return
        
        self.time = 0
        self.fidx = 0
        self.attack = True
        player_whip = whip.Whip(self.draw_pos, self.look_left)
        player_whip.sound.set_volume(10)
        player_whip.sound.play()
        gfw.world.add(gfw.layer.whip, player_whip)

    def move(self):
        if self.state in [Player.CROUCH, Player.CROUCH_MOVE]:
            self.state = Player.CROUCH_MOVE
        elif self.state in [Player.IDLE]:
            self.state = Player.MOVE
        else:
            return

    def jump(self):
        if self.state in [Player.JUMP, Player.FALLING]: return
        else:
            self.state = Player.JUMP
            self.jump_on = True
            self.jump_sound.play()

    def dameged_just(self):
        if self.dameged_time > 0:return
        else: 
            self.life = max(0,self.life -1)
            self.dameged_time = 1
        self.jump_speed = 1.0
        self.rope_on = False
        self.hit_sound.play()

        if self.life is 0:
            self.wall_grab = False
            self.state = Player.STUN_DEATH

    def dameged_to_stun(self):
        if self.dameged_time > 0:return
        else:
            self.life = max(0,self.life -1)
            self.dameged_time = 1
        self.hit_sound.play()
        self.state = Player.DAMAGED
        self.time = 0
        self.fidx = 0
        self.jump_speed += 0.5
        self.rope_on = False
        self.dameged = True
        self.wall_grab = False
        if self.life is 0:
            self.state = Player.STUN_DEATH

    def dameged_to_die(self):
        if self. life > 0:
            self.life = 0
        self.time = 0
        self.fidx = 0
        self.jump_speed += 0.5
        self.rope_on = False
        self.dameged = True
        self.wall_grab = False

    def recover(self):
        if self.time > 1:
            self.dameged = False
            self.stun = False
            self.state = Player.IDLE

    def increase_score(self, score):
        self.score += score

    def get_ledder(self):
        dx = 0
        ledder = None
        x,y = self.draw_pos
        _,P_bottom,_,P_top = self.get_bb()
        for tile in gfw.world.objects_at(gfw.layer.tile):
            if tile.name in ['entrance', 'exit','cave_block', 'arrow_block', 'spike']: continue
            l,b,r,t = tile.get_bb()
            if x > r or x < l: continue
            if tile.name is 'ledder_top' and y > t and y < t + tile.unit and self.crouch == -1 : 
                self.rope_on = True
                self.jump_speed = -1
                ledder = tile
            if y < b or y > t + 20: continue
            if self.crouch == 1:
                self.rope_on = True
                self.jump_speed = 1
            elif self.crouch == -1 and self.rope_on == True:
                self.jump_speed = -1
            elif self.crouch == 0 and self.rope_on is True:
                self.jump_speed = 0
                if self.attack == False:
                    self.time = 0
                    self.fidx = 0
            if self.rope_on is True:
                dx = x - (l + tile.unit // 2)
            if ledder is None:
                ledder = tile

        return dx, ledder

    def get_floor(self):
        if self.jump_on == True and self.jump_time < 0.3:
            self.jump_speed = 1.5
            self.jump_time += gfw.delta_time
        else:
            self.jump_time = 0
            self.jump_on = False

        x, y = self.draw_pos
        _,_,_,P_top = self.get_bb()
        for tile in gfw.world.objects_at(gfw.layer.tile):
            if tile.name in ['entrance', 'exit','ledder_bottom','ledder_top', 'rope_top', 'rope_mid', 'rope_last']: continue
            l,b,r,t = tile.get_bb()
            if x > r + 10 or x < l - 10: continue
            gab = (b + t) // 2
            if y > gab: continue
            if P_top < b:
                pass
            else:
                if self.jump_speed > 0:
                    self.jump_speed = 0
                    self.jump_on = False
                    self.jump_time = 0

    def get_tile(self, foot):
        selected = None
        sel_top = 0
        x,y = self.draw_pos
        for tile in gfw.world.objects_at(gfw.layer.tile):
            if tile.name in ['entrance', 'exit','ledder_bottom', 'rope_top', 'rope_mid', 'rope_last']: continue
            if tile.name == 'ledder_top' and self.rope_on is True: continue
            l,b,r,t = tile.get_bb()
            if x < l - 10 or x > r + 10: continue
            gab = (b + t) // 2 + 5
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
            self.jump_speed -= GRAVITY * gfw.delta_time   # 중력 적용
            if self.state in [Player.DAMAGED, Player.STUN_DEATH, Player.ATTACK]: return dy
            if self.jump_speed > 0:
                self.state = Player.JUMP
            else:
                self.state = Player.FALLING
        else:
            # print('falling', t, foot)
            if self.jump_speed <= 0 and int(foot) < t:
                if tile.name == 'spike':
                    self.life = 0
                    self.spike_sound.play()
                dy = t - foot
                if self.state is Player.DAMAGED: self.state = Player.STUN_DEATH
                else: self.state = Player.MOVE
                self.jump_speed = 0
                self.rope_on = False
                # print('Now running', t, foot)
        return dy

    def get_wall(self, left, right):
        selected = None
        _,y = self.draw_pos
        for tile in gfw.world.objects_at(gfw.layer.tile):
            if tile.name in ['entrance', 'exit','ledder_bottom','ledder_top', 'spike', 'rope_top', 'rope_mid', 'rope_last']: continue
            l,b,r,t = tile.get_bb()
            if y > t or y < b: continue
            if right < l or left > r: continue
            selected = tile
        return selected

    def wall_check(self, wall,left, right):
        x,y = self.draw_pos
        if wall is not None:
            l,b,r,t = wall.get_bb()
            if self.dx == -1 and r > left and l < left:
                self.mag = 0
            elif self.dx == 1 and l < right and l > left:
                self.mag = 0
            else:
                self.mag = 2
            gab = (t + b) // 2
            if y > gab and self.jump_speed <= 0:
                if self.wall_grab == True:
                    self.wall_grab = True
                    self.jump_speed = 0
                    return
                if self.dx == -1 and r > left and l < left:
                    self.pos = r - self.size // 2 , t
                    self.wall_grab = True
                    self.jump_speed = 0
                elif self.dx == 1 and l < right and l > left:
                    self.pos = l - self.size // 2 , t
                    self.wall_grab = True
                    self.jump_speed = 0
        else:
            self.mag = 2

    