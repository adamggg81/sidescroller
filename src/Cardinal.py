import pygame
import math
import Geometry as Geometry
import globals as GLOBAL
from Character import Character
from Enemy import Enemy
from WorldObjects import WorldObjects


class Cardinal(Enemy):
    def __init__(self, x, y):

        # call init for Enemy
        super().__init__(x, y)

        self.width = 80
        self.height = 40
        self.speed = 8
        self.jump_power = -5
        self.jumping = False
        self.floor_kills = False
        self.bounce_off_walls = True

        self.jump_on_head = True
        self.change_direction_timer = 0
        self.change_direction_threshold = 0.75

        self.player_bonded = False
        self.lock_position = 0
        self.trigger = False

        self.platform_bonding_threshold = 0.5
        self.platform_bonding_timer = self.platform_bonding_threshold

        # self.image = pygame.image.load("player.png").convert_alpha()
        image_list = ["cardinal_right.png", "cardinal_left.png"]
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

        player = world_objects.Player

        if not self.trigger:
            self.y = self.initial_y
            self.vel_y = 0
            if abs(self.x - player.x) <= GLOBAL.SCREEN_WIDTH/2:
                self.y = player.y-GLOBAL.SCREEN_HEIGHT/2
                self.trigger = True
                if self.x > player.x:
                    self.current_direction = -1
                else:
                    self.current_direction = 1

        if not self.trigger:
            return

        self.vel_x = self.current_direction * self.speed
        if self.y > player.y and not self.player_bonded:
            self.y = player.y
            self.vel_y = 0
            self.player_bonded = True
            self.lock_position = player.y

        if self.player_bonded:
            self.vel_y = 0
            self.y = self.lock_position

        if self.stun_timer < self.stun_threshold:
            self.vel_x = 0
