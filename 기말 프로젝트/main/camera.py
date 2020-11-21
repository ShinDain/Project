import gfw
from player import Player
from pico2d import *
import gobj

FULL_MAP_WIDTH = 2560
FULL_MAP_HEIGHT = 2048

def update(player):
	p_x, p_y = player.pos
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
		bottom_gab = 0
		p_draw_y = p_y
	elif p_y > FULL_MAP_HEIGHT - ch // 2:
		bottom_gab = FULL_MAP_HEIGHT - ch
		p_draw_y = p_y - bottom_gab
	else: 
		bottom_gab = p_y - (ch // 2)
		p_draw_y = ch // 2
		
	return p_draw_x, p_draw_y, left_gab, bottom_gab


	
	
	