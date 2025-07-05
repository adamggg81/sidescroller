import pygame
import globals as GLOBAL
import Geometry as Geometry
from WorldObjects import WorldObjects


class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 0
        self.jump_power = 0
        self.jumping = False
        self.gravity = GLOBAL.gravity
        self.on_ground = False
        self.floor_kills = True
        self.alive = True
        self.invincible_timer = 0
        self.invincible_threshold = 1.5
        self.stun_threshold = 1
        self.stun_timer = self.stun_threshold
        self.initial_x = x
        self.initial_y = y
        self.image_number = 0
        self.image_list = []
        self.image = None
        self.rect = None

    def update(self, world_objects: WorldObjects):
        original_ground_status = self.on_ground
        original_y = self.y
        # Apply gravity
        self.vel_y += self.gravity

        # Update position
        self.x += self.vel_x
        self.y += self.vel_y

        self.on_ground = False

        is_killed = False

        self.invincible_timer = self.invincible_timer + 1 / world_objects.fps
        if self.invincible_timer > self.invincible_threshold:
            self.invincible_timer = self.invincible_threshold

        self.stun_timer = self.stun_timer + 1 / world_objects.fps
        if self.stun_timer > self.stun_threshold:
            self.stun_timer = self.stun_threshold

        # Ground collision (simple floor at bottom of screen)
        if self.y + self.height >= GLOBAL.WORLD_HEIGHT - GLOBAL.GROUND_HEIGHT:
            self.y = GLOBAL.WORLD_HEIGHT - GLOBAL.GROUND_HEIGHT - self.height
            # self.vel_y = 0
            self.on_ground = True

            # check if floor kills
            if self.floor_kills:
                is_killed = True

        [is_on_platform, target_platform, wall_collision] = Geometry.platform_collision(self, world_objects.platforms)
        if is_on_platform:
            self.y = target_platform.rect.y - self.height
            self.on_ground = True
        elif wall_collision == -1:
            self.x = target_platform.rect.x - self.width
            self.vel_x = 0
        elif wall_collision == 1:
            self.x = target_platform.rect.x + target_platform.rect.width
            self.vel_x = 0

        if self.on_ground:
            self.vel_y = 0
        if original_ground_status and self.on_ground:
            self.y = original_y

        # Keep player within world boundaries
        if self.x < 0:
            self.x = 0
            self.vel_x = -1 * self.vel_x
        elif self.x + self.width > GLOBAL.WORLD_WIDTH:
            self.x = GLOBAL.WORLD_WIDTH - self.width
            self.vel_x = -1*self.vel_x

        if self.y < 0:
            self.y = 0
            self.vel_y = 0

        self.personal_update(world_objects)

        if is_killed:
            self.die()

    def die(self):
        pass

    def personal_update(self, world_objects: WorldObjects):
        pass

    def on_screen(self, camera):
        result = False
        in_x = False
        in_y = False
        if self.x+self.width > camera.x and self.x < camera.x + GLOBAL.SCREEN_WIDTH:
            in_x = True
        if self.y+self.height > camera.y and self.y < camera.y + GLOBAL.SCREEN_HEIGHT:
            in_y = True
        if in_x and in_y:
            result = True

        return result
