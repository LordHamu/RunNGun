import pygame
from pygame import *

class Camera(object):
    def __init__(self, width, height):
        self.rect = Rect(0, 0, width, height)
        
    def apply(self, target):
        return target.rect.move(self.rect.topleft)

    def update(self, target):
        self.rect = self.camera_func(self.rect, target.rect)

    def on_camera(self, target):
        import constants
        on_cam = bool(Rect(0, 0, constants.DWIDTH, constants.DHEIGHT).colliderect(self.apply(target)))
        if on_cam:
            return True
        else:
            return False

    def camera_func(self, camera, target_rect):
        import constants
        l, t, _, _ = target_rect
        _, _, w, h = camera
        l, t, _, _ = -l+constants.HALF_WIDTH, -t+constants.HALF_HEIGHT, w, h

        l = min(0, l)                                  # stop scrolling at the left edge
        l = max(-(camera.width-constants.DWIDTH), l)   # stop scrolling at the right edge
        t = max(-(camera.height-constants.DHEIGHT), t) # stop scrolling at the bottom
        t = min(0, t)                                  # stop scrolling at the top
        return Rect(l, t, w, h)
