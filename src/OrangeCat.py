import pygame
import math
import Geometry as Geometry
import globals as GLOBAL
from Character import Character
from Enemy import Enemy
from Hairball import Hairball
from WorldObjects import WorldObjects


class OrangeCat(Enemy):
    def __init__(self, x, y):

        # call init for Enemy
        super().__init__(x, y)

        self.width = 74
        self.height = 57
        self.speed = 2
        # OrangeCat jump power is only to bounce when enemy jumps up into his feet
        self.jump_power = -20
        self.jumping = False
        self.floor_kills = False

        self.x_range = 200
        self.y_range = 75

        self.jump_on_head = True
        self.health = 2
        self.current_direction = -1
        self.is_shooting = False
        self.shoot_timer = 0
        self.shoot_threshold = 2

        self.platform_bonding_threshold = 0.5
        self.platform_bonding_timer = self.platform_bonding_threshold

        image_list = ["orange_cat_right.png", "orange_cat_left.png"]
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

        if self.is_shooting or self.shoot_timer > 0:
            self.shoot_timer = self.shoot_timer + 1 / world_objects.fps
            if self.shoot_timer > self.shoot_threshold:
                self.shoot_timer = 0

        player = world_objects.Player
        x_diff1 = abs(self.x - player.x - player.width)
        x_diff2 = abs(self.x + self.width - player.x)
        y_diff1 = abs(self.y - player.y - player.height)
        y_diff2 = abs(self.y + self.height - player.y)
        self.is_shooting = False
        x_in_range = False
        y_in_range = False
        if x_diff1 <= self.x_range or x_diff2 <= self.x_range:
            x_in_range = True
        if y_diff1 <= self.y_range or y_diff2 <= self.y_range:
            y_in_range = True
        if x_in_range and y_in_range and self.stun_timer >= self.stun_threshold:
            # Only shoot if already facing player
            facing_player = False
            if self.x > player.x and self.current_direction == -1:
                facing_player = True
            if self.x < player.x and self.current_direction == 1:
                facing_player = True
            if facing_player:
                self.is_shooting = True
                self.vel_x = 0
                if self.x > player.x:
                    self.image_number = 1
                    self.current_direction = -1
                else:
                    self.image_number = 0
                    self.current_direction = 1

        if self.is_shooting and self.shoot_timer == 0:
            new_ball = Hairball(0, self.y)
            if self.x > player.x:
                x_start = self.x - new_ball.width - 1
            else:
                x_start = self.x + self.width + 1
            new_ball.x = x_start
            world_objects.Enemy.append(new_ball)

        if not self.is_shooting:
            self.vel_x = self.current_direction * self.speed
            if self.on_ground and self.current_platform is not None and self.platform_bonding_timer >= self.platform_bonding_threshold:
                platform = self.current_platform
                platform_min = platform.x
                platform_max = platform_min + platform.width
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
