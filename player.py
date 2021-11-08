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
from shot import Shot


class Player(pygame.sprite.Sprite):
    def __init__(self, game, screen):
        super(Player, self).__init__()
        self.image = pygame.image.load("./assets/bishop.png").convert()
        # self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.game = game
        self.update()

    def create_shot(self):
        return Shot(self.game, self.rect.x, self.rect.y, math.radians(self.get_direction()))

    def get_direction(self):
        mouse_x, mouse_y = self.game.mouse.get_pos()
        old_x, old_y = self.rect.x, self.rect.y
        angle = math.atan2(old_y - mouse_y, old_x - mouse_x) * (180/math.pi)
        return angle

    def update(self):
        SCREEN_WIDTH, SCREEN_HEIGHT = self.game.display.get_surface().get_size()

        pressed_keys = self.game.key.get_pressed()

        old_x, old_y = self.rect.x, self.rect.y
        angle = self.get_direction()
        self.surf = self.game.transform.rotate(
            self.image.convert_alpha(), -angle)

        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = old_x, old_y

        if pressed_keys[K_UP] or pressed_keys[K_w]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN] or pressed_keys[K_s]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT