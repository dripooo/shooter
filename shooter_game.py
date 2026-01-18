# import and init
import pygame
pygame.init()

from soldier import Soldier
from bullet import Bullet
# screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooter Game")

# clock
clock = pygame.time.Clock()
FPS = 60

# variables

background_color = (25,0,0)
game_is_running = True

# player
player_1 = Soldier(char_type="player", x_pos=400, y_pos=400, scale=2, speed=5)
enemy_1 = Soldier(char_type="enemy", x_pos=400, y_pos=400, scale=2, speed=5)

# create sprite bullet group
bullet_group = pygame.sprite.Group()

# game loop
while game_is_running:
    clock.tick(FPS)

    screen.fill(background_color)
    bullet_group.update()
    bullet_group.draw(screen)
    # --- PLAYER --- and move rect conditionally

    if player_1.is_alive:
        if player_1.shoot:
            

            player_1.shoot_a_bullet(screen_width=SCREEN_WIDTH, bullet_group=bullet_group)

        if player_1.is_airborne:
            player_1.update_action(2)
        elif player_1.moving_left or player_1.moving_right:
            player_1.update_action(1)
        else:
            player_1.update_action(0)
    

        player_1.move()
    player_1.update_player()
    player_1.draw(screen)


    # --- ENEMY ---
    enemy_1.update_animation()
    enemy_1.draw(screen)

    # --- EVENTS ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_is_running = False

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                player_1.moving_right = True
                pass
            if event.key in (pygame.K_LEFT, pygame.K_a):
                player_1.moving_left = True
                pass
            if event.key == pygame.K_SPACE and player_1.is_alive:
                player_1.jump = True
                pass
            if event.key == pygame.K_m:
                player_1.shoot = True

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                player_1.moving_right = False
            if event.key in (pygame.K_LEFT, pygame.K_a):
                player_1.moving_left = False
            if event.key == pygame.K_m:
                player_1.shoot = False

    pygame.display.update()

# quit pygame
pygame.quit()


