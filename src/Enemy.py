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

        self.current_direction = 0
        self.change_direction_timer = 0
        self.change_direction_threshold = 0.75

    def personal_update(self, world_objects: WorldObjects):

        # Call the specific enemy update routine
        self.enemy_update(world_objects)

        # Run all global enemy update code
        # 1:  Enemy to Enemy collision
        for enemy in world_objects.Enemy:
            if enemy != self:
                if Geometry.character_collision(self, enemy):
                    bounce_mult = 2
                    if self.x > enemy.x:
                        self.current_direction = 1
                        enemy.current_direction = -1
                        enemy.x = self.x - enemy.width
                    else:
                        self.current_direction = -1
                        enemy.current_direction = 1
                        enemy.x = self.x + self.width
                    self.vel_x = self.current_direction * bounce_mult * self.speed
                    enemy.vel_x = enemy.current_direction * bounce_mult * enemy.speed
                    self.change_direction_timer = 0
                    enemy.change_direction_timer = 0
                    break

    def enemy_update(self, world_objects: WorldObjects):
        pass
