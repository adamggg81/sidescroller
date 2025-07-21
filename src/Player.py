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
        self.max_health = 3
        self.health = self.max_health
        self.floor_kills = True
        self.god_mode = False
        self.respawn_timer = 0
        self.respawn_threshold = 1
        self.allow_user_control = True
        self.control_timer = 0
        self.control_threshold = 0.2
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
        self.health = self.max_health
        self.alive = True
        self.invincible_timer = 0
        # reload the current level on respawn
        world_objects.load_level(world_objects.current_level)

    def personal_update(self, world_objects: WorldObjects):

        self.respawn_timer = self.respawn_timer + 1 / world_objects.fps
        if self.respawn_timer > self.respawn_threshold:
            self.respawn_timer = self.respawn_threshold

        self.control_timer = self.control_timer + 1 / world_objects.fps
        if self.control_timer > self.control_threshold:
            self.control_timer = self.control_threshold
            self.allow_user_control = True

        if not self.alive:
            if self.respawn_timer == self.respawn_threshold:
                self.respawn(world_objects)
            return

        # check reaching Goal
        # Eventually it will have to load a new level, but just "die" for now
        goal = world_objects.Goal
        if Geometry.rectangle_rectangle_intersection(self.rect_list(), goal.rect_list()):
            # force previous frame y position to be above box (jump in box)
            # collide with sides of box
            if self.x+self.width-self.vel_x <= goal.x:
                self.x = goal.x - self.width
            elif self.x-self.vel_x >= goal.x+goal.width:
                self.x = goal.x + goal.width
            elif self.y+self.height >= goal.y+goal.height-goal.y_offset:
                self.die()


        # Test new enemy collision system with bounce back
        head_hit = False
        target_enemy = None
        enemy_collision = False
        for enemy in world_objects.Enemy:
            if self.character_collision(enemy):
                target_enemy = enemy
                enemy_collision = True
                if enemy.collision_kills:
                    enemy.die()
                direction_change = False
                if self.y + self.height - self.vel_y <= enemy.y - enemy.vel_y:
                    # self jumps on top of enemy
                    self.vel_y = 0.75 * self.jump_power
                    self.y = enemy.y - self.height
                    enemy.vel_y = 0
                    head_hit = True
                elif enemy.y + enemy.height - enemy.vel_y <= self.y - self.vel_y:
                    # enemy jumps on top of self
                    enemy.vel_y = 0.75 * enemy.jump_power
                    # special case:  enemy has no jump power: instead redirect self
                    if enemy.jump_power == 0:
                        self.vel_y = -1 * self.vel_y / 10
                    else:
                        self.vel_y = 0
                elif self.x > enemy.x:
                    # self is right of enemy
                    #self.current_direction = 1
                    enemy.current_direction = -1
                    direction_change = True
                    #self.x = enemy.x + enemy.width
                    self.vel_x = self.speed
                else:
                    # self is left of enemy
                    #self.current_direction = -1
                    enemy.current_direction = 1
                    direction_change = True
                    #self.x = enemy.x - self.width
                    self.vel_x = -1*self.speed
                if direction_change:
                    #self.vel_x = self.current_direction * self.speed
                    enemy.vel_x = enemy.current_direction * enemy.speed
                    #self.change_direction_timer = 0
                    enemy.change_direction_timer = 0
                # reset platform bonding timer on collision
                #self.platform_bonding_timer = 0
                enemy.platform_bonding_timer = 0
                break

        # resolve non-movement details of collision
        # 1) dealing damage to enemy when jumping on its head (when applicable)
        # 2) dealing damage to player
        if enemy_collision:
            take_damage = True
            if head_hit and target_enemy.jump_on_head:
                take_damage = False
                # enemy takes damage (unless the debug global flag is set to false)
                # enemy doesn't take damage if stunned
                if target_enemy.stun_timer >= target_enemy.stun_threshold and GLOBAL.enemy_takes_damage:
                    target_enemy.health = target_enemy.health - 1
                target_enemy.stun_timer = 0
                if target_enemy.health <= 0:
                    target_enemy.die()
            if self.god_mode:
                take_damage = False
            if take_damage:
                if self.invincible_timer == self.invincible_threshold:
                    self.health = self.health - 1
                    # Quirk:  need to also set invincible timer to 0  because of the way die function operates
                    # May need to change this behavior
                    self.invincible_timer = 0
                    self.allow_user_control = False
                    self.control_timer = 0
                    # give the bounce back a little y-velocity.  looks better
                    if self.on_ground:
                        self.vel_y = self.jump_power / 3


        # bounce_up = False
        # top_bounce = world_objects.height
        # for enemy in world_objects.Enemy:
        #     if self.character_collision(enemy):
        #         # Test code for making enemy die upon player collision.  Not finished.  Testing for Hairball
        #         if enemy.collision_kills:
        #             enemy.die()
        #         if enemy.jump_on_head:
        #             if self.y + self.height - self.vel_y <= enemy.y - enemy.vel_y:
        #                 if enemy.y - self.height < top_bounce:
        #                     top_bounce = enemy.y - self.height
        #                 bounce_up = True
        #                 enemy.vel_y = 0
        #                 enemy.stun_timer = 0
        #             else:
        #                 if self.invincible_timer == self.invincible_threshold:
        #                     self.health = self.health - 1
        #                     self.invincible_timer = 0
        #         else:
        #             if self.invincible_timer == self.invincible_threshold:
        #                 self.health = self.health - 1
        #                 # Quirk:  need to also set invincible timer to 0  because of the way die function operates
        #                 # May need to change this behavior
        #                 self.invincible_timer = 0
        #
        # # There was a bug when multiple enemies were bounced upon
        # # After setting position and velocity for the first collision, the second caused death
        # # The fix is to wait until after all collisions are resolved to set position and velocity
        # if bounce_up:
        #     self.vel_y = 0.75*self.jump_power
        #     self.y = top_bounce

        # Resolve health
        if self.health <= 0:
            self.invincible_timer = self.invincible_threshold
            self.die()

    def jump(self):
        if self.on_ground and not self.jumping:
            self.vel_y = self.jump_power
        # Wall jump check
        if self.on_wall and not self.jumping:
            self.vel_y = self.jump_power
            self.vel_x = self.speed * self.wall_side
            self.allow_user_control = False
            # Using the same timer as enemy bounce back.  Maybe need a different timer eventually
            self.control_timer = 0
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
