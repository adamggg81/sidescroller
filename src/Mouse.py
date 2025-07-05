import pygame
import math
import Geometry as Geometry
import globals as GLOBAL
from Character import Character
from Enemy import Enemy
from WorldObjects import WorldObjects


class Mouse(Enemy):
    def __init__(self, x, y):

        # call init for Enemy
        super().__init__(x, y)

        self.width = 50
        self.height = 34
        self.speed = 2
        self.jump_power = 0
        self.jumping = False
        self.floor_kills = False
        self.jump_timer = 0
        self.jump_threshold = 1.2

        self.jump_on_head = True
        self.current_direction = 0
        self.change_direction_timer = 0
        self.change_direction_threshold = 0.75

        # self.image = pygame.image.load("player.png").convert_alpha()
        image_list = ["mouse_right.png"]
        for j in range(len(image_list)):
            self.image_list.append(pygame.image.load(image_list[j]).convert_alpha())
            self.image_list[j].set_colorkey(GLOBAL.WHITE)

        self.image = self.image_list[0]

        self.rect = self.image.get_rect()

    def draw(self, screen, camera):
        screen_x = self.x - camera.x
        screen_y = self.y - camera.y

        self.rect.center = (screen_x + self.width / 2, screen_y + self.height / 2)
        screen.blit(self.image, self.rect)

    def enemy_update(self, world_objects: WorldObjects):
        pass
