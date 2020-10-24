from pico2d import *
import gfw

Tile = []

def enter():
    global image
    image = load_image('res/kpu_1280x960.png')

def update():
    pass

def draw():
    image.draw(500, 400)
    image.clip_draw(100,100,200,800, 1100,400)
    for i in range(len(Tile)):
    	image.clip_draw(100,100,100,100, *Tile[i])

def handle_event(e):
	#global Tile
    if e.type == SDL_QUIT:
        gfw.quit()
    elif (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
        gfw.quit()
    if (e.type, e.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT):
    	if(e.x < 1000):
    		Tx = e.x // 100
    		Ty = (get_canvas_height() - e.y - 1) // 100
    		Tile.append((Tx * 100 + 50,Ty * 100 + 50))
    	else:
    		pass # 블럭 선택 지점 구현예정 
def exit():
    global image
    del image

def pause():
    pass
def resume():
    pass
    
if __name__ == '__main__':
    gfw.run_main()


# 만든 맵 저장 구현 