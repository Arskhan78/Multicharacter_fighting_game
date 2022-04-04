from cgitb import grey
from turtle import right
import pygame
import sys
from pygame.locals import *
import random
import time

pygame.init()
clock = pygame.time.Clock()

width = 1000
height = 500

screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("Rapid Fire 1v1 Pong")

# Colors
Dark_grey = (24, 24, 24)
white = (255, 255, 255)

# Rectangles
x_center = 500
y_center = 250
ball = pygame.Rect(x_center - 10, y_center - 10, 20, 20)
player_1 = pygame.Rect(15, y_center - 40, 15, 80)
hitbox_1 = pygame.Rect(0, 0, 15, 500)
player_2 = pygame.Rect(970, y_center - 40, 15, 80)
hitbox_2 = pygame.Rect(985, 0, 15, 500)
font = pygame.font.Font('assets/font/pixelfont.ttf', 70)
baby_font = pygame.font.Font('assets/font/pixelfont.ttf', 30)
player1_score = 0
player2_score = 0

#random list coler switching
player_colors = [(24, 221, 228), (129, 24, 228), (139, 64, 255)]
colour_one = random.randint(0, 2)
colour_two = random.randint(0, 2)

# when ball collides with player
def player_interactions():
    global ball_speed_x
    if ball.colliderect(player_1) or ball.colliderect(player_2):
        ball_speed_x *= -1

#when a player has scored
def scored():
    global ball_speed_x, ball_speed_y, player1_score, player2_score
    if ball.colliderect(hitbox_1):
        ball.x = x_center - 10
        ball.y = y_center - 10
        ball_speed_x = 0
        ball_speed_y = 0
        player_1.y = y_center - 40
        player_2.y = y_center - 40
        player2_score += 1
        while ball_speed_x == 0:
            ball_speed_x = random.randint(-6, 6)
        ball_speed_y = random.randint(1, 5)

    if ball.colliderect(hitbox_2):
        ball.x = x_center - 10
        ball.y = y_center - 10
        ball_speed_x = 0
        ball_speed_y = 0
        player_1.y = y_center - 40
        player_2.y = y_center - 40
        player1_score += 1
        # loop
        while ball_speed_x == 0:
            ball_speed_x = random.randint(-6, 6)
        ball_speed_y = random.randint(1, 5)

# ball collides with borders
def game_ball():
    global ball_speed_x
    global ball_speed_y

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= height:
        ball_speed_y *= -1
    if ball.left <= 0 or ball.right >= width:
        ball_speed_x *= -1


# same loop
ball_speed_x = random.randint(-6, 6)
while ball_speed_x == 0:
    ball_speed_x = random.randint(-6, 6)
ball_speed_y = random.randint(1, 5)
screen_index = 1

run = True
# game loop
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
        if event.type == pygame.KEYDOWN:
            if screen_index == 1 and event.key == K_SPACE:
                screen_index = 2
            if event.key == K_UP:
                moving_UP = True
            if event.key == K_DOWN:
                moving_DOWN = True
            if event.key == K_TAB:
                moving_UP2 = True
            if event.key == K_LSHIFT:
                moving_DOWN2 = True
        else:
            moving_UP = False
            moving_UP2 = False
            moving_DOWN = False
            moving_DOWN2 = False

    if screen_index == 1:
        screen.fill(Dark_grey)
        play_text = font.render("Press SPACE to play", False, white)
        screen.blit(play_text, (300, 100))

        controltext_player_1 = baby_font.render(
            "For Player on the RIGHT, Press TAB to move up and LSHIFT to move down",
            False,
            white)
        screen.blit(controltext_player_1, (205, 400))

        controltext_player_2 = baby_font.render(
            "For Player on the left, Press UP-ARROW to move up and DOWN-Arrow to move down",
            False,
            white)
        screen.blit(controltext_player_2, (200, 250))

    if screen_index == 2:
        # player 1
        if player_1.top >= 0 and moving_UP:
            player_1.y -= 10
        if player_1.bottom <= 500 and moving_DOWN:
            player_1.y += 10

        # player 2
        if player_2.top >= 0 and moving_UP2:
            player_2.y -= 10
        if player_2.bottom <= 500 and moving_DOWN2:
            player_2.y += 10

        player_score_1 = 0
        player_score_2 = 0
        # scoring

        # funtions
        game_ball()
        player_interactions()
        scored()

        screen.fill(Dark_grey)

        # drawings

        pygame.draw.rect(screen, player_colors[colour_one], player_1)
        pygame.draw.rect(screen, player_colors[colour_two], player_2)
        pygame.draw.aaline(screen, white, (x_center, 0), (x_center, height))
        pygame.draw.rect(screen, white, ball)
        pygame.draw.rect(screen, 'red', hitbox_1)
        pygame.draw.rect(screen, 'red', hitbox_2)
        score_text = font.render(f"{player1_score}", False, white)
        score_text_2 = font.render(f"{player2_score}", False, white)
        screen.blit(score_text, (450, 50))
        screen.blit(score_text_2, (525, 50))

    pygame.display.flip()
    clock.tick(144)
