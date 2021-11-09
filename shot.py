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
        self.speed = SPEED
        direction.scale_to_length(self.speed)
        self.direction_vector = direction
        self.damage = DAMAGE

    def update(self):
        self.rect.move_ip(self.direction_vector)
        SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()

        if self.rect.left < 0 - 100 or self.rect.right > SCREEN_WIDTH + 100 or self.rect.top <= 0 - 100 or self.rect.bottom >= SCREEN_HEIGHT + 100:
            self.kill()
