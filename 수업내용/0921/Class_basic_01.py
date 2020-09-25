from pico2d import *

class Grass:
	def __init__(self):
		self.image = load_image('../res/grass.png')
	def draw(self):
		self.image.draw(400,30)

class Boy:
	def __init__(self, x = 0, y = 85, dx = 2):
		self.image = load_image('../res/animation_sheet.png')
		self.x, self.y = x , y
		self.fidx = 0
		self.dx = dx
		self.action = 0


	def draw(self):
		self.image.clip_draw(self.fidx * 100, 100 * self.action, 100, 100, self.x, self.y)
	def update(self):
		self.x += self.dx
		self.fidx = (self.fidx + 1) % 8
		if self.x % 100 == 0:
			self.action = (self.action + 1) % 4
		
open_canvas()

# type name = UpperCamelCase
# method name = lowerCamelCase

grass = Grass()

boy = Boy()
b2 = Boy(get_canvas_width(), 200, -2)

objects = [grass, boy, b2]

running = True
while running:
    clear_canvas()
    # for o in objects:
    # 	o.draw()

    	# if o is Grass:
    	# 	o.image.draww(400,300)
    	# else:
    	#	o.image.clip_draw(100 * o.fidx, 100 * o.action,100,100,o.x,85)
    	# 다형성은 분기를 하지 않는것이 핵심

    grass.draw()
    boy.draw()
    b2.draw()
    # grass.draw(400,30)
    # boy.ch.clip_draw(boy.fidx * 100, 100 * boy.action , 100,100,boy.x,85)
    # b2.ch.clip_draw(b2.fidx * 100, 100 * b2.action , 100,100,b2.x,85)
    update_canvas()

    evts = get_events()
    for e in evts:
        if e.type == SDL_KEYDOWN:
            if e.key == SDLK_ESCAPE:
                running = False
        elif e.type == SDL_QUIT:
            running = False

    boy.update()

    b2.update()

    if boy.x > get_canvas_width():
    	running = False

    if b2.x < 0:
    	running = False

    delay(0.01)

close_canvas()
