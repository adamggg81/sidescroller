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
        # Mouse jump power is only to bounce when enemy jumps up into Mouse's feet
        self.jump_power = -20
        self.jumping = False
        self.floor_kills = False
        self.jump_timer = 0
        self.jump_threshold = 1.2

        self.jump_on_head = True
        self.current_direction = 1
        self.change_direction_timer = 0
        self.change_direction_threshold = 0.75

        self.platform_bonding_threshold = 0.5
        self.platform_bonding_timer = self.platform_bonding_threshold

        # self.image = pygame.image.load("player.png").convert_alpha()
        image_list = ["mouse_right.png", "mouse_left.png"]
        for j in range(len(image_list)):
            self.image_list.append(pygame.image.load(image_list[j]).convert_alpha())
            self.image_list[j].set_colorkey(GLOBAL.WHITE)

        self.image = self.image_list[0]

        self.rect = self.image.get_rect()

    def draw(self, screen, camera):
        screen_x = self.x - camera.x
        screen_y = self.y - camera.y

        if self.vel_x > 0:
            self.image_number = 0
        elif self.vel_x < 0:
            self.image_number = 1

        self.image = self.image_list[self.image_number]

        self.rect.center = (screen_x + self.width / 2, screen_y + self.height / 2)
        screen.blit(self.image, self.rect)

    def enemy_update(self, world_objects: WorldObjects):

        self.vel_x = self.current_direction * self.speed
        if self.on_ground and self.current_platform is not None and self.platform_bonding_timer >= self.platform_bonding_threshold:
            platform = self.current_platform
            platform_min = platform.rect.x
            platform_max = platform_min + platform.rect.width
            if self.vel_x > 0 and self.x + self.width > platform_max:
                self.vel_x = -1*self.speed
                self.x = platform_max - self.width
                self.current_direction = -1
            elif self.vel_x < 0 and self.x < platform_min:
                self.vel_x = self.speed
                self.x = platform_min
                self.current_direction = 1

        if self.stun_timer < self.stun_threshold:
            self.vel_x = 0
