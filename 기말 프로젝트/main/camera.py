import gfw
from player import Player
from pico2d import *
import gobj

FULL_MAP_WIDTH = 2560
FULL_MAP_HEIGHT = 2048

def camera_init():
	global camera_time
	camera_time = 0

def update(player):
	global camera_time

	p_x, p_y = player.pos
	p_c = player.crouch
	cw = get_canvas_width()
	ch = get_canvas_height()

	p_draw_x, p_draw_y = p_x, p_y
	left_gab = 0
	bottom_gab = 0

	if p_x < cw // 2:
		left_gab = 0
		p_draw_x = p_x
	elif p_x > FULL_MAP_WIDTH - cw // 2:
		left_gab = FULL_MAP_WIDTH - cw
		p_draw_x = p_x - left_gab
	else: 
		left_gab = p_x - (cw // 2)
		p_draw_x = cw // 2

	if p_y < ch // 2:
		bottom_gab = -10
		p_draw_y = p_y
	elif p_y > FULL_MAP_HEIGHT - ch // 2:
		bottom_gab = FULL_MAP_HEIGHT - ch
		p_draw_y = p_y - bottom_gab
	else: 
		bottom_gab = p_y - (ch // 2)
		p_draw_y = ch // 2

	if player.state in [Player.LOOKUP, Player.CROUCH] and player.fidx is len(player.anim) - 1:
		camera_time += gfw.delta_time
		camera_time = clamp(0,camera_time,2)
		if camera_time > 1:
			p_draw_y += p_c * -500 * (camera_time - 1)
			bottom_gab += p_c * 500 * (camera_time - 1)
	else:
		camera_time = 0
	
	return p_draw_x, p_draw_y, left_gab, bottom_gab


	
	
	