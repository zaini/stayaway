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
import random

SPEED = 10


class Shot(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direction, offset_angle=0, size=10, damage=50, speed=10):
        super(Shot, self).__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.speed = SPEED
        direction.scale_to_length(self.speed)
        self.direction_vector = direction.rotate(offset_angle)
        self.damage = damage

    def update(self):
        self.image.fill((random.randint(0, 255), random.randint(
            0, 255), random.randint(0, 255)))

        self.rect.move_ip(self.direction_vector)
        SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()

        if self.rect.left < 0 - 100 or self.rect.right > SCREEN_WIDTH + 100 or self.rect.top <= 0 - 100 or self.rect.bottom >= SCREEN_HEIGHT + 100:
            self.kill()
