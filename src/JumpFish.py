import pygame
import math
import Geometry as Geometry
import globals as GLOBAL
from Character import Character
from Enemy import Enemy
from WorldObjects import WorldObjects


class JumpFish(Enemy):
    def __init__(self, x, y):

        # call init for Enemy
        super().__init__(x, y)

        self.width = 40
        self.height = 60
        self.speed = 0
        self.jump_power = -15
        self.jumping = False
        self.floor_kills = False
        self.jump_timer = 0
        self.jump_threshold = 3
        self.sink_in_floor = True
        self.gravity = GLOBAL.gravity / 4

        self.jump_on_head = True

        image_list = ["jump_fish_up.png", "jump_fish_down.png"]
        for j in range(len(image_list)):
            self.image_list.append(pygame.image.load(image_list[j]).convert_alpha())
            self.image_list[j].set_colorkey(GLOBAL.WHITE)

        self.image = self.image_list[0]

        self.rect = self.image.get_rect()

    def draw(self, screen, camera):
        screen_x = self.x - camera.x
        screen_y = self.y - camera.y

        if self.vel_y <= 0:
            self.image_number = 0
        elif self.vel_y > 0:
            self.image_number = 1

        self.image = self.image_list[self.image_number]

        self.rect.center = (screen_x + self.width / 2, screen_y + self.height / 2)
        screen.blit(self.image, self.rect)

    def enemy_update(self, world_objects: WorldObjects):
        # reset x velocity when frog is on the ground
        # it continues moving in whatever horizontal direction during a jump
        if self.on_ground:
            self.vel_x = 0

        # whenever the jump_timer crosses the jump_threshold, frog is allowed to jump again
        self.jump_timer = self.jump_timer + 1/world_objects.fps
        if self.jump_timer > self.jump_threshold:
            self.jump_timer = self.jump_threshold

        if self.on_ground and self.jump_timer >= self.jump_threshold:
            self.vel_y = self.jump_power
            self.jump_timer = 0
