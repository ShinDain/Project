import gfw
from pico2d import *
import gobj

class HorzScrollBackground:
    def __init__(self, imageName):
        self.imageName = imageName
        self.image = gfw.image.load(gobj.res(imageName))
        self.cw, self.ch = get_canvas_width(), get_canvas_height()
        self.scroll = 0
        self.speed = 0

    def update(self):
        self.scroll += self.speed * gfw.delta_time

    def set_scroll(self, scroll):
        self.scroll = scroll

    def draw(self):
        left, bottom = 0, 0
        page = self.image.w * self.ch // self.image.h
        curr = int(-self.scroll) % page
        if curr > 0:
            sw = int(1 + self.image.h * curr / self.ch)
            sl = self.image.w - sw
            src = sl, 0, sw, self.image.h
            dw = int(sw * self.ch / self.image.h)
            dst = curr - dw, 0, dw, self.ch
            self.image.clip_draw_to_origin(*src, *dst)
        dst_width = round(self.image.w * self.ch / self.image.h)
        while curr + dst_width < self.cw:
            dst = curr, 0, dst_width, self.ch
            self.image.draw_to_origin(*dst)
            curr += dst_width
        if curr < self.cw:
            dw = self.cw - curr
            sw = int(1 + self.image.h * dw / self.ch)
            src = 0, 0, sw, self.image.h
            dw = int(sw * self.ch / self.image.h)
            dst = curr, 0, dw, self.ch
            self.image.clip_draw_to_origin(*src, *dst)

    def to_screen(self, point):
        x, y = point
        return x - self.scroll, y

    def translate(self, point):
        x, y = point
        return x + self.scroll, y

    def get_boundary(self):
        return (-sys.maxsize, -sys.maxsize, sys.maxsize, sys.maxsize)