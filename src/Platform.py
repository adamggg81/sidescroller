import pygame


class Platform:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.grass_image = pygame.image.load("grass_platform.png").convert_alpha()
        self.dirt_image = pygame.image.load("dirt_platform.png").convert_alpha()

    def draw(self, screen, camera):
        screen_x = self.x - camera.x
        screen_y = self.y - camera.y
        # pygame.draw.rect(screen, GLOBAL.GREEN, (screen_x, screen_y, self.rect.width, self.rect.height))

        platform_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        for y_offset in range(0, self.height + 1, 20):
            for x_offset in range(0, self.width + 1, 20):
                if y_offset == 0:
                    platform_surface.blit(self.grass_image, (x_offset, 0))
                else:
                    platform_surface.blit(self.dirt_image, (x_offset, y_offset))
        screen.blit(platform_surface, (screen_x, screen_y))
