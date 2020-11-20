import gfw
from pico2d import *
import gobj

class Background:
    def __init__(self, imageName):
        self.imageName = imageName
        self.image = gfw.image.load(gobj.res(imageName))
        self.cw, self.ch = get_canvas_width(), get_canvas_height()
        self.win_rect = 0, 0, self.cw, self.ch
        self.center = self.image.w // 2, self.image.h // 2
        hw, hh = self.cw // 2, self.    ch // 2
        self.boundary = hw, hh, self.image.w - hw, self.image.h - hh
    def draw(self):
        self.image.clip_draw_to_origin(*self.win_rect, 0, 0)
    def update(self):
        sl = round(tx - self.cw / 2)
        sb = round(ty - self.ch / 2)
        self.win_rect = sl, sb, self.cw, self.ch
    def get_boundary(self):
        return self.boundary
    def translate(self, point):
        x, y = point
        l, b, r, t = self.win_rect
        return l + x, b + y
    def to_screen(self, point):
        # return self.cw // 2, self.ch // 2
        x, y = point
        l, b, r, t = self.win_rect
        return x - l, y - b

class InfiniteBackground(Background):
    def __init__(self, imageName,center_object, width=0, height=0):
        super().__init__(imageName)
        self.boundary = (-sys.maxsize, -sys.maxsize, sys.maxsize, sys.maxsize)
        self.center_object_pos = center_object
        self.fix_x, self.fix_y = self.cw // 2, self.ch // 2
        if width == 0:
            width = self.image.w
        if height == 0:
            height = self.image.h
        self.w, self.h = width, height
    def set_fixed_pos(self, x, y):
        self.fix_x, self.fix_y = x, y
    def update(self):
        object_cx, object_cy = self.center_object_pos
        # quadrant 3
        q3l = round(object_cx - self.fix_x) % self.image.w
        q3b = round(object_cy - self.fix_y) % self.image.h
        q3w = clamp(0, self.image.w - q3l, self.image.w)
        q3h = clamp(0, self.image.h - q3b, self.image.h)
        self.q3rect = q3l, q3b, q3w, q3h
        # quadrant 2
        self.q2rect = q3l, 0, q3w, self.ch - q3h
        self.q2origin = 0, q3h
        # quadrant 4
        self.q4rect = 0, q3b, self.cw - q3w, q3h
        self.q4origin = q3w, 0
        # quadrant 1
        self.q1rect = 0, 0, self.cw - q3w, self.ch - q3h
        self.q1origin = q3w, q3h

    def draw(self):
        self.image.clip_draw_to_origin(*self.q3rect, 0, 0)
        self.image.clip_draw_to_origin(*self.q2rect, *self.q2origin)
        self.image.clip_draw_to_origin(*self.q4rect, *self.q4origin)
        self.image.clip_draw_to_origin(*self.q1rect, *self.q1origin)

    def to_screen(self, point):
        x, y = point
        return self.fix_x + x, self.fix_y + y

    def translate(self, point):
        x, y = point
        dx, dy = x - self.fix_x, y - self.fix_y
        return dx, dy