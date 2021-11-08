import pygame
import math

SPEED = 2


class Enemy(pygame.sprite.Sprite):
    def __init__(self, player):
        super(Enemy, self).__init__()
        self.image = pygame.Surface((35, 35))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.player = player

    def update(self):
        dx, dy = self.rect.x - self.player.rect.x, self.rect.y - self.player.rect.y
        if dx != 0:
            dx = dx/abs(dx)
        if dy != 0:
            dy = dy/abs(dy)
        self.rect.move_ip(-dx * SPEED, -dy * SPEED)
