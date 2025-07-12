import pygame
import math
import Geometry as Geometry
import globals as GLOBAL
from Character import Character
from WorldObjects import WorldObjects


class Enemy(Character):
    def __init__(self, x, y):

        # call init for Character
        super().__init__(x, y)

        self.jump_on_head = True
        self.change_direction_timer = 0
        self.change_direction_threshold = 0.75

        self.platform_bonding_threshold = 0
        self.platform_bonding_timer = 0

    def die(self):
        self.alive = False

    def personal_update(self, world_objects: WorldObjects):

        # whenever the change direction timer crosses the threshold, frog is allowed to change direction
        self.change_direction_timer = self.change_direction_timer + 1 / world_objects.fps
        if self.change_direction_timer > self.change_direction_threshold:
            self.change_direction_timer = self.change_direction_threshold

        # platform bonding timer
        self.platform_bonding_timer = self.platform_bonding_timer + 1 / world_objects.fps
        if self.platform_bonding_timer > self.platform_bonding_threshold:
            self.platform_bonding_timer = self.platform_bonding_threshold

        # Call the specific enemy update routine
        self.enemy_update(world_objects)

        # Run all global enemy update code
        # 1:  Enemy to Enemy collision
        for enemy in world_objects.Enemy:
            if enemy != self:
                did_collide = False
                if self.character_collision(enemy):
                    did_collide = True
                if not did_collide:
                    if self.shape == 'rectangle':
                        self_center_x = self.x + self.width/2
                        self_center_y = self.y + self.height/2
                        self_reach = max(self.width, self.height)/2
                    elif self.shape == 'circle':
                        self_center_x = self.x + self.radius
                        self_center_y = self.y + self.radius
                        self_reach = self.radius
                    if enemy.shape == 'rectangle':
                        enemy_center_x = enemy.x + enemy.width/2
                        enemy_center_y = enemy.y + enemy.height/2
                        enemy_reach = max(enemy.width, enemy.height) / 2
                    elif enemy.shape == 'circle':
                        enemy_center_x = enemy.x + enemy.radius
                        enemy_center_y = enemy.y + enemy.radius
                        enemy_reach = enemy.radius
                    enemy_distance = math.sqrt(math.pow(self_center_x - enemy_center_x, 2) + math.pow(self_center_y - enemy_center_y, 2))
                    if enemy_distance <= self_reach + enemy_reach + abs(self.vel_x) + abs(self.vel_y) + abs(enemy.vel_x) + abs(enemy.vel_y):
                        # move them back in time until a collision occurs
                        # if distance increases, quit
                        num_steps = 20
                        self_x = self.x
                        self_y = self.y
                        enemy_x = enemy.x
                        enemy_y = enemy.y
                        self.x = self.x - self.vel_x
                        self.y = self.y - self.vel_y
                        enemy.x = enemy.x - enemy.vel_x
                        enemy.y = enemy.y - enemy.vel_y
                        for j in range(num_steps):
                            self.x = self.x + self.vel_x/num_steps
                            self.y = self.y + self.vel_y / num_steps
                            enemy.x = enemy.x + enemy.vel_x / num_steps
                            enemy.y = enemy.y + enemy.vel_y / num_steps
                            if self.character_collision(enemy):
                                did_collide = True
                                break
                        self.x = self_x
                        self.y = self_y
                        enemy.x = enemy_x
                        enemy.y = enemy_y



                if did_collide:
                #if self.character_collision(enemy):
                    direction_change = False
                    if self.y + self.height - self.vel_y <= enemy.y - enemy.vel_y:
                        # self jumps on top of enemy
                        self.vel_y = 0.75 * self.jump_power
                        # special case:  self has no jump power: instead redirect enemy
                        if self.jump_power == 0:
                            enemy.vel_y = -1*enemy.vel_y/10
                        else:
                            enemy.vel_y = 0
                    elif enemy.y + enemy.height - enemy.vel_y <= self.y - self.vel_y:
                        # enemy jumps on top of self
                        enemy.vel_y = 0.75 * enemy.jump_power
                        # special case:  enemy has no jump power: instead redirect self
                        if enemy.jump_power == 0:
                            self.vel_y = -1 * self.vel_y/10
                        else:
                            self.vel_y = 0
                    elif self.x > enemy.x:
                        # self is right of enemy
                        self.current_direction = 1
                        enemy.current_direction = -1
                        direction_change = True
                    else:
                        # self is left of enemy
                        self.current_direction = -1
                        enemy.current_direction = 1
                        direction_change = True
                    if direction_change:
                        self.vel_x = self.current_direction * self.speed
                        enemy.vel_x = enemy.current_direction * enemy.speed
                        self.change_direction_timer = 0
                        enemy.change_direction_timer = 0
                    # reset platform bonding timer on collision
                    self.platform_bonding_timer = 0
                    enemy.platform_bonding_timer = 0
                    break

    def enemy_update(self, world_objects: WorldObjects):
        pass
