import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from player import Player
from enemy import Enemy
import random
import math

pygame.init()
pygame.font.init()

WAVE_FONT = pygame.font.SysFont('Comic Sans MS', 20)
HEALTH_FONT = pygame.font.SysFont('Comic Sans MS', 20)
DEATH_FONT = pygame.font.SysFont('Comic Sans MS', 30)
DEATH_TEXT_SURFACE = DEATH_FONT.render(
    "YOU HAVE DIED", False, (0, 0, 255))
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

player = Player(screen)

shot_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

wave = 0
waves = {
    0: 5,
    500: 10,
    1000: 20,
    1500: 40
}

kills = 0


def is_enemy_shot(shot, enemy):
    global kills
    KNOCKBACK_DISTANCE = 100
    if enemy.rect.colliderect(shot.rect):
        enemy.take_damage(shot.damage)
        if enemy.is_dead():
            kills += 1
        else:
            dy = enemy.rect.center[1] - shot.rect.center[1]
            dx = enemy.rect.center[0] - shot.rect.center[0]

            dirvect = pygame.math.Vector2(dx, dy)
            if dy != 0:
                dirvect.normalize()
                dirvect.scale_to_length(KNOCKBACK_DISTANCE)
                enemy.rect.move_ip(dirvect)

        return True
    return False


shooting = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                player.dash()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            shooting = True
        elif event.type == pygame.MOUSEBUTTONUP:
            shooting = False
        elif event.type == pygame.QUIT:
            running = False

    # update
    if not player.is_dead():
        if shooting:
            shot_group.add(player.create_shot())

        collisions = pygame.sprite.groupcollide(
            shot_group, enemy_group, True, False, collided=is_enemy_shot)

        player.update()
        shot_group.update()
        if wave in waves:
            for n in range(waves[wave]):
                OFFSET = 100
                enemy_group.add(random.choice([Enemy(player, OFFSET, random.randint(OFFSET, SCREEN_HEIGHT)),
                                               Enemy(player, SCREEN_WIDTH - OFFSET,
                                                     random.randint(OFFSET, SCREEN_HEIGHT)),
                                               Enemy(player, random.randint(
                                                   OFFSET, SCREEN_WIDTH), OFFSET),
                                               Enemy(player, random.randint(OFFSET, SCREEN_WIDTH), SCREEN_HEIGHT - OFFSET)]))
        enemy_group.update()
        wave += 1

    # draw
    screen.fill((0, 0, 0))
    screen.blit(player.surf, (player.rect.x -
                              (player.surf.get_width() // 2), player.rect.y -
                              (player.surf.get_height() // 2)))

    shot_group.draw(screen)
    enemy_group.draw(screen)

    wave_text_surface = WAVE_FONT.render(
        "WAVE: {}".format(wave), False, (0, 255, 0))
    screen.blit(wave_text_surface, (0, 0))

    health_text_surface = HEALTH_FONT.render(
        "HEALTH: {}".format((player.health / player.max_health) * 100), False, (0, 255, 0))
    screen.blit(health_text_surface, (0, SCREEN_HEIGHT -
                                      health_text_surface.get_height()))

    kills_text_surface = WAVE_FONT.render(
        "KILLS: {}".format(kills), False, (0, 0, 255))
    screen.blit(kills_text_surface, (0, wave_text_surface.get_height()))
    if player.is_dead():
        screen.blit(DEATH_TEXT_SURFACE, (SCREEN_WIDTH //
                                         2 - (DEATH_TEXT_SURFACE.get_width() // 2), 0))

    pygame.display.flip()
    clock.tick(75)

pygame.quit()
