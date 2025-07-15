import pygame
import math
import globals as GLOBAL
import Geometry as Geometry
from WorldObjects import WorldObjects
from Platform import Platform


class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape = 'rectangle'
        self.width = 0
        self.height = 0
        self.radius = 0
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 0
        self.jump_power = 0
        self.jumping = False
        self.gravity = GLOBAL.gravity
        self.obey_gravity = True
        self.on_ground = False
        self.floor_kills = True
        self.alive = True
        self.current_direction = 0
        self.bounce_off_walls = False
        self.invincible_timer = 0
        self.invincible_threshold = 1.5
        self.stun_threshold = 1
        self.stun_timer = self.stun_threshold
        self.current_platform = None
        self.collision_kills = False
        self.initial_x = x
        self.initial_y = y
        self.image_number = 0
        self.image_list = []
        self.image = None
        self.rect = None

    def position_update(self):
        # Apply gravity
        if self.obey_gravity:
            self.vel_y += self.gravity

        # Update position
        self.x += self.vel_x
        self.y += self.vel_y

    def update(self, world_objects: WorldObjects):

        self.on_ground = False

        is_killed = False

        self.invincible_timer = self.invincible_timer + 1 / world_objects.fps
        if self.invincible_timer > self.invincible_threshold:
            self.invincible_timer = self.invincible_threshold

        self.stun_timer = self.stun_timer + 1 / world_objects.fps
        if self.stun_timer > self.stun_threshold:
            self.stun_timer = self.stun_threshold

        # Ground collision (simple floor at bottom of screen)
        top_ground = world_objects.height - GLOBAL.GROUND_HEIGHT
        if self.y + self.height >= top_ground:
            self.y = top_ground - self.height
            self.on_ground = True
            self.current_platform = None

            # check if floor kills
            if self.floor_kills:
                is_killed = True

        [is_on_platform, target_platform, wall_collision] = self.platform_collision(world_objects.platforms)
        if is_on_platform:
            self.y = target_platform.y - self.height
            self.on_ground = True
            self.current_platform = target_platform
        elif wall_collision == -1:
            self.x = target_platform.x - self.width
        elif wall_collision == 1:
            self.x = target_platform.x + target_platform.width
        if abs(wall_collision) == 1:
            if self.bounce_off_walls:
                self.vel_x = -1*self.vel_x
                self.current_direction = -1*self.current_direction
            else:
                self.vel_x = 0
        # if collision kills, die on platform collision
        if self.collision_kills and target_platform is not None:
            self.die()

        # set y velocity to 0 if on the ground
        # also if gravity tries to push through the ground, reset y position
        if self.on_ground:
            self.vel_y = 0

        # Keep player within world boundaries
        if self.x < 0:
            self.x = 0
            self.vel_x = -1 * self.vel_x
            self.current_direction = 1
            if self.collision_kills:
                self.die()
        elif self.x + self.width > world_objects.width:
            self.x = world_objects.width - self.width
            self.vel_x = -1*self.vel_x
            self.current_direction = -1
            if self.collision_kills:
                self.die()

        # Check hitting the "Ceiling"
        if self.y < 0:
            self.y = 0
            self.vel_y = 0

        self.personal_update(world_objects)

        if is_killed:
            self.die()

    def character_collision(self, aggressor):
        result = False
        if not isinstance(aggressor, Character):
            raise ValueError("Aggressor must also be a Character type")
        if self.shape == 'rectangle' and aggressor.shape == 'rectangle':
            if Geometry.rectangle_rectangle_intersection(self.rect_list(), aggressor.rect_list()):
                result = True
        elif self.shape == 'rectangle' and aggressor.shape == 'circle':
            if Geometry.rectangle_circle_intersection(self.rect_list(), aggressor.circle_list()):
                result = True
        elif self.shape == 'circle' and aggressor.shape == 'rectangle':
            if Geometry.rectangle_circle_intersection(aggressor.rect_list(), self.circle_list()):
                result = True
        elif self.shape == 'circle' and aggressor.shape == 'circle':
            if Geometry.circle_circle_intersection(self.circle_list(), aggressor.circle_list()):
                result = True

        return result

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

    def rect_list(self):
        return [self.x, self.y, self.width, self.height]

    def circle_list(self):
        return [self.x, self.y, self.radius]

    def platform_collision(self, platforms):
        result = False
        collision_platform = None
        wall_collision = 0
        past_player_bottom = self.y - self.vel_y + self.height
        current_player_bottom = self.y + self.height
        for platform in platforms:
            if not isinstance(platform, Platform):
                raise ValueError("platform must be a Platform")
            if Geometry.rectangle_rectangle_intersection(self.rect_list(), platform.rect_list()):
                # Landing on top of platform
                if self.vel_y > 0 and self.y < platform.y and past_player_bottom <= platform.y + 5:
                    result = True
                    collision_platform = platform
                    return result, collision_platform, wall_collision
                elif self.x + self.width - self.vel_x <= platform.x:
                    wall_collision = -1
                    collision_platform = platform
                    return result, collision_platform, wall_collision
                elif self.x - self.vel_x >= platform.x + platform.width:
                    wall_collision = 1
                    collision_platform = platform
                    return result, collision_platform, wall_collision

        # special check for high velocity moving through the platform
        for platform in platforms:
            if abs(self.vel_y) > platform.height:
                platform_top = platform.y
                platform_bottom = platform.y + platform.height

                if past_player_bottom < platform_top and current_player_bottom > platform_bottom:

                    num_steps = math.ceil(abs(self.vel_y) / platform.height)
                    x_step = self.vel_x / num_steps
                    y_step = self.vel_y / num_steps
                    for j in range(num_steps - 1):
                        this_x = self.x - self.vel_x + x_step * (j + 1)
                        this_y = self.y - self.vel_y + y_step * (j + 1)
                        past_player_rect = [this_x, this_y, self.width, self.height]
                        if Geometry.rectangle_rectangle_intersection(past_player_rect, platform.rect_list()):
                            # Landing on top of platform
                            if self.vel_y > 0 and self.y < platform.y:
                                result = True
                                collision_platform = platform
                                return result, collision_platform, wall_collision

        return result, collision_platform, wall_collision
