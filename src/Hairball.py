import pygame
import math
import Geometry as Geometry
import globals as GLOBAL
from Character import Character
from Enemy import Enemy
from WorldObjects import WorldObjects


class Hairball(Enemy):
    def __init__(self, x, y):

        # call init for Enemy
        super().__init__(x, y)

        self.width = 20
        self.height = 20
        self.radius = 10
        self.shape = 'circle'
        self.speed = 10
        self.obey_gravity = False
        self.initialize = True
        self.jump_on_head = False
        self.bounce_off_walls = True

        image_list = ["orange_hairball.png"]
        for j in range(len(image_list)):
            self.image_list.append(pygame.image.load(image_list[j]).convert_alpha())
            self.image_list[j].set_colorkey(GLOBAL.WHITE)

        self.image = self.image_list[0]

        self.rect = self.image.get_rect()

    def draw(self, screen, camera):
        screen_x = self.x - camera.x
        screen_y = self.y - camera.y

        self.image = self.image_list[0]

        self.rect.center = (screen_x + self.width / 2, screen_y + self.height / 2)
        screen.blit(self.image, self.rect)

    def enemy_update(self, world_objects: WorldObjects):

        if self.initialize:
            if self.x >= world_objects.Player.x:
                self.current_direction = -1
            else:
                self.current_direction = 1
            self.initialize = False

        self.vel_x = self.current_direction * self.speed
