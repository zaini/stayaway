import pygame
import math

SPEED = 2
HEALTH = 500
DAMAGE = 5
SIZE = 80


class Enemy(pygame.sprite.Sprite):
    def __init__(self, player, x, y):
        super(Enemy, self).__init__()
        self.image = pygame.image.load("./assets/enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (SIZE, SIZE))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.player = player
        self.health = HEALTH
        self.damage = DAMAGE
        self.speed = SPEED

    def is_dead(self):
        return self.health <= 0

    def take_damage(self, damage):
        self.health -= damage

    def update(self):
        if self.is_dead():
            self.kill()

        dx, dy = self.rect.x - self.player.rect.x, self.rect.y - self.player.rect.y
        dirvect = pygame.math.Vector2(-dx, -dy)
        if dy != 0:
            dirvect.normalize()
            dirvect.scale_to_length(self.speed)
            self.rect.move_ip(dirvect)

        if pygame.sprite.collide_mask(self, self.player):
            self.player.take_damage(self.damage)

        self.rect.clamp_ip(self.player.screen.get_rect())
