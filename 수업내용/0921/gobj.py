import random
from pico2d import *

class Grass:
	def __init__(self):
		self.image = load_image('grass.png')
	def draw(self):
		self.image.draw(400,30)

class Boy:
    def __init__(self):
        self.image = load_image('animation_sheet.png')
        self.x = random.randint(0,300)
        self.y = random.randint(0,300)  
        self.dx = random.random() # 0.0 ~ 1.0
        self.dy = random.random() # 0.0 ~ 1.0
        self.fidx = random.randint(0,7)
        self.action = random.randint(0,3)
    def draw(self):
        self.image.clip_draw(self.fidx * 100, 100 * self.action, 100, 100, self.x, self.y)
    def update(self):
        self.x += self.dx
        self.y += self.dy

        self.fidx = (self.fidx + 1) % 8

        if self.x % 100 == 0:
            self.action = (self.action + 1) % 4


if __name__ == '__main__':
    print("I am the main")
else:
    print("i am imported")
