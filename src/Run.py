import pygame
import sys
import math
from Player import Player
from Platform import Platform
from Frog import Frog
from Mouse import Mouse
from Cardinal import Cardinal
from Hairball import Hairball
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
        # Platform(200, floor - 800, 100, 800),
        # Platform(700, floor - 600, 100, 800),
        Platform(200, floor-150, 150, 20),
        Platform(400, floor-250, 150, 80),
        Platform(600, floor-330, 150, 40),
        Platform(400, floor-450, 150, 20),
        Platform(800, floor-200, 150, 20),
        Platform(1000, floor-300, 150, 20),
        Platform(1200, floor-400, 150, 250),
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
    # enemy_list.append(Frog(400, floor-100))
    # enemy_list.append(Hairball(500, floor - 100))
    enemy_list.append(Frog(800, floor-250-40))
    enemy_list.append(Frog(2100, floor - 250 - 40))
    enemy_list.append(Mouse(600, 800))
    enemy_list.append(Frog(1250, 750))
    enemy_list.append(Cardinal(1200, 200))
    enemy_list.append(Hairball(800, floor-300))
    enemy_list.append(Hairball(900, floor - 400))
    enemy_list.append(Hairball(1000, floor - 500))
    enemy_list.append(Hairball(1100, floor - 600))

    jump_keys = [pygame.K_SPACE, pygame.K_UP, pygame.K_w]

    actual_fps = GLOBAL.FPS

    world_objects = WorldObjects()
    world_objects.Player = player
    world_objects.camera = camera
    world_objects.platforms = platforms
    world_objects.Enemy = enemy_list
    world_objects.fps = actual_fps

    background_image = pygame.image.load("forest_background.png")

    # Test loading level
    world_objects.load_level('levels\\sandbox1.txt')

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

        # Update x, y, vel_y for each moving object
        player.position_update()
        for enemy in world_objects.Enemy:
            enemy.position_update()

        # Update player
        player.update(world_objects)
        
        # Update camera to follow player
        camera.update(player)

        for enemy in world_objects.Enemy:
            enemy.update(world_objects)

        # Remove dead enemies
        world_objects.delete_dead_enemies()
        
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
        for platform in world_objects.platforms:
            platform.draw(screen, camera)

        for enemy in world_objects.Enemy:
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
