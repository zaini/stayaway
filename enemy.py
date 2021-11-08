import pygame
import math

SPEED = 2
HEALTH = 100
DAMAGE = 20
SIZE = 35


class Enemy(pygame.sprite.Sprite):
    def __init__(self, player, x, y):
        super(Enemy, self).__init__()
        self.image = pygame.Surface((SIZE, SIZE))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.player = player
        self.health = HEALTH
        self.damage = DAMAGE

    def is_dead(self):
        return self.health <= 0

    def take_damage(self, damage):
        self.health -= damage

    def update(self):
        if self.is_dead():
            self.kill()

        dx, dy = self.rect.x - self.player.rect.x, self.rect.y - self.player.rect.y
        if dx != 0:
            dx = dx/abs(dx)
        if dy != 0:
            dy = dy/abs(dy)
        self.rect.move_ip(-dx * SPEED, -dy * SPEED)

        if self.player.rect.colliderect(self):
            self.player.take_damage(self.damage)
