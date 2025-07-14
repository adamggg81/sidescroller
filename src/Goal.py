import pygame
import math
import globals as GLOBAL
import Geometry as Geometry
from WorldObjects import WorldObjects
from Platform import Platform


class Goal:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 65
        self.height = 75
        # the box image needs to "sink" into the ground a bit to look right
        self.y_offset = 10
        self.image_list = []
        self.image_number = 0

        image_list = ["Goal.png"]
        for j in range(len(image_list)):
            self.image_list.append(pygame.image.load(image_list[j]).convert_alpha())
            self.image_list[j].set_colorkey(GLOBAL.WHITE)

        self.image = self.image_list[0]

        self.rect = self.image.get_rect()

    def draw(self, screen, camera):
        screen_x = self.x - camera.x
        screen_y = self.y - camera.y

        self.image = self.image_list[self.image_number]

        self.rect.center = (screen_x + self.width / 2, screen_y + self.height / 2 + self.y_offset)
        screen.blit(self.image, self.rect)
