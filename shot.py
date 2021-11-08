import pygame
from pygame.locals import (
    K_w,
    K_a,
    K_s,
    K_d,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
import math

SPEED = 10
DAMAGE = 30
SIZE = 10


class Shot(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direction):
        super(Shot, self).__init__()
        self.image = pygame.Surface((SIZE, SIZE))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.direction = direction
        self.damage = DAMAGE
        self.dx = math.cos(self.direction)
        self.dy = math.cos(math.pi/2 - self.direction)

    def update(self):
        self.rect.x -= SPEED * self.dx
        self.rect.y -= SPEED * self.dy
        SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()

        if self.rect.left < 0 - 100 or self.rect.right > SCREEN_WIDTH + 100 or self.rect.top <= 0 - 100 or self.rect.bottom >= SCREEN_HEIGHT + 100:
            self.kill()
