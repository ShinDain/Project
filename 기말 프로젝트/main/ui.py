import gfw
from pico2d import *
import gobj

uiimage = None
object_rects = {}
font = None

def load():
    global font, uiimage
    font = gfw.font.load('res/Tekton-Bold.otf', 40)
    global objectimage
    if uiimage is None:
        uiimage = gfw.image.load(gobj.res('ui_icon.png'))

class Ui:
    def __init__(self, player):
        self.player_life = player.life
        self.boom_count = player.boom_count
        self.rope_count = player.rope_count

        self.score = player.score
        self.pos = get_canvas_width() // 2 + 100, get_canvas_height() - 50

        self.life_rect = (0,0,32,32)
        self.boom_rect = (32,0,32,32)
        self.rope_rect = (64,0,32,32)
        self.score_rect = (96,0,32,32)
    def update(self):
        pass

    def draw(self):
        x, y = self.pos
        uiimage.clip_draw(*self.life_rect,x - 500,y, 50,50)
        uiimage.clip_draw(*self.boom_rect,x - 300,y, 50,50)
        uiimage.clip_draw(*self.rope_rect,x - 100,y, 50,50)
        uiimage.clip_draw(*self.score_rect,x + 100,y, 50,50)
        font.draw(x - 510,y, '     : %d' % self.player_life)
        font.draw(x - 310,y, '     : %d' % self.boom_count)
        font.draw(x - 120,y, '     : %d' % self.rope_count)
        font.draw(x + 80,y, '     : %d' % self.score)

    def set_count(self, player):
        self.player_life = player.life
        self.boom_count = player.boom_count
        self.rope_count = player.rope_count
        self.score = player.score

