import random
from pico2d import *
import gfw
import gobj

def collide(a,b):
	left_a,bottom_a,right_a,top_a = a.get_bb()
	left_b,bottom_b,right_b,top_b = b.get_bb()

	if left_a > right_b:return False
	if right_a < left_b:return False
	if top_a < bottom_b:return False
	if bottom_a > top_b:return False

	return True

def active_arrow(a,b):
	if b.name is not 'arrow_block': return
	left_a,bottom_a,right_a,top_a = a.get_bb()
	left_b,bottom_b,right_b,top_b = b.get_active_bb()

	if left_a > right_b:return False
	if right_a < left_b:return False
	if top_a < bottom_b:return False
	if bottom_a > top_b:return False

	return True

def collide_check_whip(player):
    # 채찍과 오브젝트 충돌체크
    for layer in range(gfw.layer.box, gfw.layer.object + 1):
        for obj in gfw.world.objects_at(layer):
            for i in gfw.world.objects_at(gfw.layer.whip):
                crash = collide(obj,i)
                if crash == True:
                    print('fjd')
                    obj.collide_whip(player.pos)

def collide_check_monster(player):
    # 플레이어와 몬스터 충돌체크 
    for M in gfw.world.objects_at(gfw.layer.monster):
        crash = collide(M,player)
        if crash == True:
            player.dameged_to_stun()

def collide_check_object(player):
    # 플레이어와 오브젝트 충돌체크 
    for obj in gfw.world.objects_at(gfw.layer.object):
        crash = collide(obj,player)
        if crash == True:
            dameged = obj.collide(player.pos)
            if dameged == True:
                player.dameged_to_stun()

def collide_check_trap():
    # 함정 발동 
    for layer in range(gfw.layer.object, gfw.layer.player + 1):
        for obj in gfw.world.objects_at(layer):
            for t in gfw.world.objects_at(gfw.layer.tile):
                crash = active_arrow(obj,t)
                if crash == True:
                    t.active()