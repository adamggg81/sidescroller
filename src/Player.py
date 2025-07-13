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
        self.respawn_timer = 0
        self.respawn_threshold = 1
        # self.jumping = False
        # self.gravity = 0.8
        # self.on_ground = False
        # self.alive = True
        # self.initial_x = x
        # self.initial_y = y
        # self.image_list = []
        self.image_list_invincible = []

        # self.image = pygame.image.load("player.png").convert_alpha()
        image_list = ["coco_right.png", "coco_left.png"]
        for j in range(len(image_list)):
            self.image_list.append(pygame.image.load(image_list[j]).convert_alpha())
            self.image_list[j].set_colorkey(GLOBAL.WHITE)

            invincible_image = image_list[j].replace('.png', '_invincible.png')
            self.image_list_invincible.append(pygame.image.load(invincible_image).convert_alpha())
            self.image_list_invincible[j].set_colorkey(GLOBAL.WHITE)

        self.image = self.image_list[0]

        self.rect = self.image.get_rect()

    def die(self):
        if self.god_mode:
            return
        if self.invincible_timer < self.invincible_threshold:
            return
        if not self.alive:
            return
        self.alive = False
        self.respawn_timer = 0

    def respawn(self, world_objects: WorldObjects):
        self.x = self.initial_x
        self.y = self.initial_y
        self.vel_x = 0
        self.vel_y = 0
        self.alive = True
        self.invincible_timer = 0
        # reload the current level on respawn
        world_objects.load_level(world_objects.current_level)

    def personal_update(self, world_objects: WorldObjects):

        self.respawn_timer = self.respawn_timer + 1 / world_objects.fps
        if self.respawn_timer > self.respawn_threshold:
            self.respawn_timer = self.respawn_threshold

        if not self.alive:
            if self.respawn_timer == self.respawn_threshold:
                self.respawn(world_objects)
            return

        bounce_up = False
        top_bounce = GLOBAL.WORLD_HEIGHT
        for enemy in world_objects.Enemy:
            if self.character_collision(enemy):
                # Test code for making enemy die upon player collision.  Not finished.  Testing for Hairball
                if enemy.collision_kills:
                    enemy.die()
                if enemy.jump_on_head:
                    if self.y + self.height - self.vel_y <= enemy.y - enemy.vel_y:
                        if enemy.y - self.height < top_bounce:
                            top_bounce = enemy.y - self.height
                        bounce_up = True
                        enemy.vel_y = 0
                        enemy.stun_timer = 0
                    else:
                        self.die()
                else:
                    self.die()

        # There was a bug when multiple enemies were bounced upon
        # After setting position and velocity for the first collision, the second caused death
        # The fix is to wait until after all collisions are resolved to set position and velocity
        if bounce_up:
            self.vel_y = 0.75*self.jump_power
            self.y = top_bounce

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

        # when player is dead, don't draw anything
        if not self.alive:
            return

        if self.vel_x > 0:
            self.image_number = 0
        elif self.vel_x < 0:
            self.image_number = 1

        self.image = self.image_list[self.image_number]
        if self.invincible_timer < self.invincible_threshold:
            if math.floor(self.invincible_timer / 0.1) % 4 == 0:
                self.image = self.image_list_invincible[self.image_number]

        self.rect.center = (screen_x + self.width / 2, screen_y + self.height / 2)
        screen.blit(self.image, self.rect)
