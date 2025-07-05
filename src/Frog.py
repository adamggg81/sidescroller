import pygame
import math
import Geometry as Geometry
import globals as GLOBAL
from Character import Character
from Enemy import Enemy
from WorldObjects import WorldObjects


class Frog(Enemy):
    def __init__(self, x, y):

        # call init for Enemy
        super().__init__(x, y)

        # self.x = x
        # self.y = y
        self.width = 40
        self.height = 40
        # self.vel_x = 0
        # self.vel_y = 0
        self.speed = 2.5
        self.jump_power = -20
        self.jumping = False
        self.floor_kills = False
        self.jump_timer = 0
        self.jump_threshold = 1.2
        self.current_direction = 0
        self.change_direction_timer = 0
        self.change_direction_threshold = 0.75

        # self.image = pygame.image.load("player.png").convert_alpha()
        image_list = ["frog.png"]
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
        # reset x velocity when frog is on the ground
        # it continues moving in whatever horizontal direction during a jump
        if self.on_ground:
            self.vel_x = 0

        # whenever the jump_timer crosses the jump_threshold, frog is allowed to jump again
        self.jump_timer = self.jump_timer + 1/world_objects.fps
        if self.jump_timer > self.jump_threshold:
            self.jump_timer = 0

        # whenever the change direction timer crosses the threshold, frog is allowed to change direction
        self.change_direction_timer = self.change_direction_timer + 1 / world_objects.fps
        if self.change_direction_timer > self.change_direction_threshold:
            self.change_direction_timer = self.change_direction_threshold

        if self.on_ground and self.on_screen(world_objects.camera) and self.stun_timer >= self.stun_threshold:
            # Follow the player
            # But there is a lag based on change_direction timer to prevent it looking so robotic
            # Exception for when the frog will jump so it doesn't jump away
            if self.change_direction_timer == self.change_direction_threshold or self.jump_timer == 0:
                if self.x > world_objects.Player.x:
                    self.current_direction = -1
                else:
                    self.current_direction = 1
                self.change_direction_timer = 0
                self.vel_x = self.current_direction * self.speed
            else:
                self.vel_x = self.current_direction * self.speed

            # when the jump timer refreshes, jump again
            if self.jump_timer == 0:
                self.vel_y = self.jump_power

