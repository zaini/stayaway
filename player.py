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

SPEED = 5
HEALTH = 10000
DASH_DISTANCE = 300


class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        super(Player, self).__init__()
        self.image = pygame.image.load("./assets/bishop.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.max_health = HEALTH
        self.screen = screen
        self.health = float(HEALTH)
        self.speed = SPEED
        self.dash_distance = DASH_DISTANCE

    def is_dead(self):
        return self.health <= 0

    def take_damage(self, damage):
        self.health = max(0, self.health - damage)

    def create_shot(self, offset_angle=0, size=10, damage=30, speed=10):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx, dy = mouse_x - self.rect.x, mouse_y - self.rect.y
        dir_vec = pygame.math.Vector2(dx, dy)
        dir_vec.normalize()
        return Shot(self.rect.x, self.rect.y, dir_vec, offset_angle=offset_angle, size=size, speed=speed, damage=damage)

    """Returns angle to mouse in degrees"""

    def get_direction(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        old_x, old_y = self.rect.x, self.rect.y
        angle = math.atan2(old_y - mouse_y, old_x - mouse_x) * (180/math.pi)
        if angle < 0:
            angle += 360
        return angle

    def dash(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        old_x, old_y = self.rect.x, self.rect.y
        dy, dx = old_y - mouse_y, old_x - mouse_x
        dirvect = pygame.math.Vector2(-dx, -dy)
        if dy != 0:
            dirvect.normalize()
        dirvect.scale_to_length(self.dash_distance)
        self.rect.move_ip(dirvect)

    def update(self):
        SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()

        pressed_keys = pygame.key.get_pressed()

        old_x, old_y = self.rect.x, self.rect.y
        angle = self.get_direction()
        self.surf = pygame.transform.rotate(
            self.image.convert_alpha(), -angle)

        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = old_x, old_y

        if pressed_keys[K_UP] or pressed_keys[K_w]:
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[K_DOWN] or pressed_keys[K_s]:
            self.rect.move_ip(0, self.speed)
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.rect.move_ip(self.speed, 0)

        # Keep player on the screen
        # self.rect.clamp_ip(self.screen.get_rect())
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.left > SCREEN_WIDTH:
            self.rect.left = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.top >= SCREEN_HEIGHT:
            self.rect.top = SCREEN_HEIGHT
