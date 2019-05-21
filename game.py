# With reference to Keith Galli's How to Program a Game! (in Python)
# Script written by Cheng Hui

import pygame
import sys
import random

# Initialize PyGame
pygame.init()

WIDTH = 800
HEIGHT = 600
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255, 0)
BACKGROUND_COLOR = (0,0,0)

player_size = 40
player_pos = [WIDTH/2, HEIGHT-2*player_size]
player_score = 0

enemy_count = 5
enemy_size = 50
enemy_pos = [random.randint(0, WIDTH-enemy_size), random.randint(0, 200)]
enemy_list = [enemy_pos]

GAME_SPEED = 10
GAME_OVER = False
DEBUG = False

clock = pygame.time.Clock()

myFont = pygame.font.SysFont("monospace", 35)

# Detect Collision Function
def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]
    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (e_x >= p_x and e_x <= p_x + player_size) or (p_x >= e_x and p_x <= e_x + enemy_size):
        if (e_y >= p_y and e_y <= p_y + player_size) or (p_y >= e_x and p_y <= e_x + enemy_size):
            return True
    return False

# Random Enemies
def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < enemy_count and delay < 0.25:
        x_pos = random.randint(0, WIDTH-enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

# Draw Enemies
def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.circle(screen, BLUE, (enemy_pos[0], enemy_pos[1]), enemy_size)

# Move All Enemies
def update_enemy_positions(enemy_list, player_score):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
            enemy_pos[1] += GAME_SPEED
        else:
            player_score += 1
            enemy_list.pop(idx)
    return player_score

def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(player_pos, enemy_pos):
            return True
    return False

def set_level(score, GAME_SPEED):
    if score < 20:
        GAME_SPEED = 10
    elif score < 40:
        GAME_SPEED = 15
    elif score < 60:
        GAME_SPEED = 20
    else:
        GAME_SPEED = 25
    return GAME_SPEED

# Setup a Screen for Game
screen = pygame.display.set_mode((WIDTH, HEIGHT))

while not GAME_OVER:

    for event in pygame.event.get():

        # Setup the Exit Button
        if event.type == pygame.QUIT:
            sys.exit()

        # Setup movement for the block
        if event.type == pygame.KEYDOWN:

            x = player_pos[0]
            y = player_pos[1]

            if event.key == pygame.K_LEFT:
                x -= player_size/2
            elif event.key == pygame.K_RIGHT:
                x += player_size/2
            elif event.key == pygame.K_UP:
                y -= player_size/2
            elif event.key == pygame.K_DOWN:
                y += player_size/2

            player_pos = [x, y]


    # Fill the screen black to disable tracking
    screen.fill(BACKGROUND_COLOR)

    # Draw player rectangle
    pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], player_size, player_size))

    # # Update position of enemy to fall down
    # if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT + 25:
    #     enemy_pos[1] += GAME_SPEED
    # else:
    #     enemy_pos[0] = random.randint(0, WIDTH - enemy_size)
    #     enemy_pos[1] = 0

    if detect_collision(player_pos, enemy_pos):
        GAME_OVER = True
        break

    drop_enemies(enemy_list)
    player_score = update_enemy_positions(enemy_list, player_score)
    GAME_SPEED = set_level(player_score, GAME_SPEED)
    draw_enemies(enemy_list)

    text = "Score: " + str(player_score)
    label = myFont.render(text, 1, YELLOW)
    screen.blit(label, (WIDTH-200, HEIGHT-40))

    if collision_check(enemy_list, player_pos):
        GAME_OVER = True
        print("Game Over: Final Score is {}.".format(player_score))
        break

    # Draw Enemy Rectangle
    # pygame.draw.circle(screen, BLUE, (enemy_pos[0], enemy_pos[1]), enemy_size)

    clock.tick(30)

    pygame.display.update()
    if DEBUG:
        print(event)