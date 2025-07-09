import pygame
import sys
import math
from Player import Player
from Frog import Frog
from Mouse import Mouse
from Cardinal import Cardinal
import globals as GLOBAL
from WorldObjects import WorldObjects

# Initialize Pygame
pygame.init()


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        
    def update(self, target):
        # Follow the target (player) horizontally
        # Keep player roughly in center of screen
        self.x = round(target.x - math.floor(GLOBAL.SCREEN_WIDTH / 2))
        
        # Clamp camera to world boundaries
        self.x = max(0, min(self.x, GLOBAL.WORLD_WIDTH - GLOBAL.SCREEN_WIDTH))

        self.y = round(target.y - math.floor(GLOBAL.SCREEN_HEIGHT / 2))
        self.y = max(0, min(self.y, GLOBAL.WORLD_HEIGHT - GLOBAL.SCREEN_HEIGHT))
        
        # # You can add vertical camera movement here if needed
        # # For now, keep camera at ground level
        # self.y = 0


class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.grass_image = pygame.image.load("grass_platform.png").convert_alpha()
        self.dirt_image = pygame.image.load("dirt_platform.png").convert_alpha()
    
    def draw(self, screen, camera):
        screen_x = self.rect.x - camera.x
        screen_y = self.rect.y - camera.y
        # pygame.draw.rect(screen, GLOBAL.GREEN, (screen_x, screen_y, self.rect.width, self.rect.height))

        platform_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)

        for y_offset in range(0, self.rect.height+1, 20):
            for x_offset in range(0, self.rect.width+1, 20):
                if y_offset == 0:
                    platform_surface.blit(self.grass_image, (x_offset, 0))
                else:
                    platform_surface.blit(self.dirt_image, (x_offset, y_offset))
        screen.blit(platform_surface, (screen_x, screen_y))


def main():
    screen = pygame.display.set_mode((GLOBAL.SCREEN_WIDTH, GLOBAL.SCREEN_HEIGHT))
    pygame.display.set_caption("Side Scroller with Camera")
    clock = pygame.time.Clock()
    
    # Create player
    player = Player(200, 400)
    
    # Create camera
    camera = Camera()
    
    # Create platforms spread across the wider world
    floor = GLOBAL.WORLD_HEIGHT
    platforms = [
        Platform(200, floor-150, 150, 20),
        Platform(400, floor-250, 150, 80),
        Platform(600, floor-330, 150, 40),
        Platform(400, floor-450, 150, 20),
        Platform(800, floor-200, 150, 20),
        Platform(1000, floor-300, 150, 20),
        Platform(1200, floor-400, 150, 20),
        Platform(1400, floor-150, 150, 20),
        Platform(1600, floor-250, 150, 20),
        Platform(1800, floor-350, 150, 20),
        Platform(2000, floor-200, 150, 20),
        Platform(2200, floor-300, 150, 20),
        Platform(250, floor - 550, 150, 20),
        Platform(400, floor - 650, 150, 20),
        Platform(750, floor - 550, 150, 20),
    ]

    # create frog
    enemy_list = []
    enemy_list.append(Frog(600, floor-300))
    enemy_list.append(Frog(800, floor-250-40))
    enemy_list.append(Frog(2100, floor - 250 - 40))
    enemy_list.append(Mouse(600, 800))
    enemy_list.append(Frog(1250, 750))
    enemy_list.append(Cardinal(1200, 200))

    jump_keys = [pygame.K_SPACE, pygame.K_UP, pygame.K_w]

    actual_fps = GLOBAL.FPS

    world_objects = WorldObjects()
    world_objects.Player = player
    world_objects.camera = camera
    world_objects.platforms = platforms
    world_objects.Enemy = enemy_list
    world_objects.fps = actual_fps

    background_image = pygame.image.load("forest_background.png")

    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYUP:
                if event.key in jump_keys:
                    player.stop_jump()

        # Handle continuous key presses
        keys = pygame.key.get_pressed()
        
        # Reset horizontal velocity
        player.stop_horizontal()
        
        # Movement controls
        if player.alive:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player.move_left()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player.move_right()
            for j in range(len(jump_keys)):
                if keys[jump_keys[j]]:
                    player.jump()
                    break

        if keys[pygame.K_g]:
            player.god_mode = True
        if keys[pygame.K_h]:
            player.god_mode = False
        
        # Update player
        player.update(world_objects)
        
        # Update camera to follow player
        camera.update(player)

        for enemy in enemy_list:
            enemy.update(world_objects)
        
        # Draw everything
        screen.fill(GLOBAL.WHITE)

        screen.blit(background_image, (0, 0))
        
        # # Draw background grid to show movement
        # for x in range(0, GLOBAL.WORLD_WIDTH, 100):
        #     screen_x = x - camera.x
        #     if -100 <= screen_x <= GLOBAL.SCREEN_WIDTH + 100:
        #         pygame.draw.line(screen, GLOBAL.GRAY, (screen_x, 0), (screen_x, GLOBAL.SCREEN_HEIGHT), 1)
        
        # Draw ground across the world
        ground_x = 0 - camera.x
        ground_width = GLOBAL.WORLD_WIDTH
        ground_y = GLOBAL.WORLD_HEIGHT - GLOBAL.GROUND_HEIGHT - camera.y
        if ground_x + ground_width > 0 and ground_x < GLOBAL.SCREEN_WIDTH:
            pygame.draw.rect(screen, GLOBAL.RED, (ground_x, ground_y, ground_width, GLOBAL.GROUND_HEIGHT))
        else:
            print('can you get here')
        
        # Draw platforms
        for platform in platforms:
            platform.draw(screen, camera)

        for enemy in enemy_list:
            enemy.draw(screen, camera)
        
        # Draw player
        player.draw(screen, camera)
        
        # Draw UI (world coordinates for debugging)
        font = pygame.font.Font(None, 20)
        text = font.render("Arrow Keys/WASD to move, Space/Up/W to jump", True, (0, 0, 0))
        screen.blit(text, (10, 10))
        
        # Show player world position
        pos_text = font.render(f"Player X: {int(player.x)}, Camera X: {int(camera.x)}, Player Y: {int(player.y)},"
                               f"Camera Y: {int(camera.y)}", True, (0, 0, 0))
        screen.blit(pos_text, (10, 50))

        # pos_text = font.render(f"Enemy2 on screen: {int(enemy_list[1].on_screen(camera))}", True, (0, 0, 0))
        # screen.blit(pos_text, (10, 100))
        
        pygame.display.flip()
        clock.tick(GLOBAL.FPS)

        # Get the actual FPS
        actual_fps = clock.get_fps()
        if actual_fps < 1:
            actual_fps = GLOBAL.FPS
        world_objects.fps = actual_fps
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
