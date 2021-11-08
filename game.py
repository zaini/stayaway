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

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

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


def test(shot, enemy):
    if enemy.rect.colliderect(shot.rect):
        enemy.take_damage(shot.damage)
        return True
    return False


running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            shot_group.add(player.create_shot())
        elif event.type == pygame.QUIT:
            running = False

    # update
    collisions = pygame.sprite.groupcollide(
        shot_group, enemy_group, True, False, collided=test)

    player.update()
    shot_group.update()
    if wave in waves:
        for n in range(waves[wave]):
            enemy_group.add(Enemy(player))
    enemy_group.update()
    wave += 1
    print(wave)
    if player.is_dead():
        print("YOU HAVE DIED")
        running = False

    # draw
    screen.fill((0, 0, 0))
    screen.blit(player.surf, (player.rect.x -
                              (player.surf.get_width() // 2), player.rect.y -
                              (player.surf.get_height() // 2)))
    shot_group.draw(screen)
    enemy_group.draw(screen)
    pygame.display.flip()
    clock.tick(75)

pygame.quit()
