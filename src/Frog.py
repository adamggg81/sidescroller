import pygame
import math
import Geometry as Geometry
import globals as GLOBAL


class Frog:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_power = -15
        self.jumping = False
        self.gravity = 0.8
        self.on_ground = False
        self.alive = True
        self.initial_x = x
        self.initial_y = y
        self.image_list = []

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

    def update(self, platforms):
        original_ground_status = self.on_ground
        original_y = self.y
        # Apply gravity
        self.vel_y += self.gravity

        # Update position
        self.x += self.vel_x
        self.y += self.vel_y

        self.on_ground = False

        # Ground collision (simple floor at bottom of screen)
        if self.y + self.height >= GLOBAL.WORLD_HEIGHT - GLOBAL.GROUND_HEIGHT:
            self.y = GLOBAL.WORLD_HEIGHT - GLOBAL.GROUND_HEIGHT - self.height
            # self.vel_y = 0
            self.on_ground = True

            # test making ground = death
            # self.alive = False

        [is_on_platform, target_platform] = Geometry.platform_collision(self, platforms)
        if is_on_platform:
            self.y = target_platform.rect.y - self.height
            self.on_ground = True

        if self.on_ground:
            self.vel_y = 0
        if original_ground_status and self.on_ground:
            self.y = original_y

        # Keep player within world boundaries
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > GLOBAL.WORLD_WIDTH:
            self.x = GLOBAL.WORLD_WIDTH - self.width

        # if not self.alive:
        #     self.reset()
