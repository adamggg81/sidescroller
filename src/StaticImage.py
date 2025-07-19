import pygame
import math
import globals as GLOBAL
import Geometry as Geometry
from WorldObjects import WorldObjects
from Platform import Platform


class StaticImage:
    def __init__(self, image_type):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.observe_camera = False

        if image_type == 'heart':
            image_file = "heart.png"
            self.width = 10
            self.height = 10
        else:
            raise ValueError("unrecognized type")

        self.image = pygame.image.load(image_file).convert_alpha()
        self.image.set_colorkey(GLOBAL.WHITE)

        self.rect = self.image.get_rect()

    def draw(self, screen, camera):
        if self.observe_camera:
            screen_x = self.x - camera.x
            screen_y = self.y - camera.y
        else:
            screen_x = self.x
            screen_y = self.y

        self.rect.center = (screen_x + self.width / 2, screen_y + self.height / 2)
        screen.blit(self.image, self.rect)
