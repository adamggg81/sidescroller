import pygame
import math
import Geometry as Geometry
import globals as GLOBAL
from Character import Character
from WorldObjects import WorldObjects


class Player(Character):
    def __init__(self, x, y):

        # call init for Character
        super().__init__(x, y)

        # self.x = x
        # self.y = y
        self.width = 40
        self.height = 60
        # self.vel_x = 0
        # self.vel_y = 0
        self.speed = 5
        self.jump_power = -15
        self.floor_kills = True
        self.god_mode = False
        # self.jumping = False
        # self.gravity = 0.8
        # self.on_ground = False
        # self.alive = True
        # self.initial_x = x
        # self.initial_y = y
        # self.image_list = []

        # self.image = pygame.image.load("player.png").convert_alpha()
        image_list = ["coco_right.png", "coco_left.png"]
        for j in range(len(image_list)):
            self.image_list.append(pygame.image.load(image_list[j]).convert_alpha())
            self.image_list[j].set_colorkey(GLOBAL.WHITE)

        self.image = self.image_list[0]

        self.rect = self.image.get_rect()

    def die(self):
        if self.god_mode:
            self.alive = True
            return
        if self.invincible_timer < self.invincible_threshold:
            return
        self.x = self.initial_x
        self.y = self.initial_y
        self.vel_x = 0
        self.vel_y = 0
        self.alive = True
        self.invincible_timer = 0

    def personal_update(self, world_objects: WorldObjects):
        for frog in world_objects.frog:
            if Geometry.character_collision(self, frog):
                if self.y + self.height - self.vel_y < frog.y - frog.vel_y:
                    self.y = frog.y - self.height
                    self.vel_y = 0.75*self.jump_power
                    frog.vel_y = 0
                    frog.stun_timer = 0
                else:
                    self.die()

    # def update(self, platforms):
    #     original_ground_status = self.on_ground
    #     original_y = self.y
    #     # Apply gravity
    #     self.vel_y += self.gravity
    #
    #     # Update position
    #     self.x += self.vel_x
    #     self.y += self.vel_y
    #
    #     self.on_ground = False
    #
    #     # Ground collision (simple floor at bottom of screen)
    #     if self.y + self.height >= GLOBAL.WORLD_HEIGHT - GLOBAL.GROUND_HEIGHT:
    #         self.y = GLOBAL.WORLD_HEIGHT - GLOBAL.GROUND_HEIGHT - self.height
    #         # self.vel_y = 0
    #         self.on_ground = True
    #
    #         # test making ground = death
    #         self.alive = False
    #
    #     [is_on_platform, target_platform] = Geometry.platform_collision(self, platforms)
    #     if is_on_platform:
    #         self.y = target_platform.rect.y - self.height
    #         self.on_ground = True
    #
    #     if self.on_ground:
    #         self.vel_y = 0
    #     if original_ground_status and self.on_ground:
    #         self.y = original_y
    #
    #     # Keep player within world boundaries
    #     if self.x < 0:
    #         self.x = 0
    #     elif self.x + self.width > GLOBAL.WORLD_WIDTH:
    #         self.x = GLOBAL.WORLD_WIDTH - self.width
    #
    #     if not self.alive:
    #         self.reset()

    def jump(self):
        if self.on_ground and not self.jumping:
            self.vel_y = self.jump_power
        # The jumping property forces release of jump key before jump can happen again
        self.jumping = True

    def stop_jump(self):
        self.jumping = False

    def move_left(self):
        self.vel_x = -self.speed

    def move_right(self):
        self.vel_x = self.speed

    def stop_horizontal(self):
        self.vel_x = 0

    def draw(self, screen, camera):
        screen_x = self.x - camera.x
        screen_y = self.y - camera.y
        # pygame.draw.rect(screen, BLUE, (screen_x, screen_y, self.width, self.height))

        if self.vel_x > 0:
            self.image = self.image_list[0]
        elif self.vel_x < 0:
            self.image = self.image_list[1]

        self.rect.center = (screen_x + self.width / 2, screen_y + self.height / 2)
        screen.blit(self.image, self.rect)
