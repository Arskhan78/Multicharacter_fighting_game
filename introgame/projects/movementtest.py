import pygame
pygame.init()
from pygame.locals import *
screen = pygame.display.set_mode((1920,1080))
pygame.display.set_caption("First Game")

player_surf = pygame.image.load('assets/playermodels/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80,300))

x = 50
y = 50
width = 40
height = 60
vel = 4
max_speed = 15 

isJump = False
jumpCount = 1

run = True


while run:
    pygame.time.delay(0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and x > 1: 
        x -= vel

    if keys[pygame.K_RIGHT] and x < 1870:  
        x += vel
        
        
    if not(isJump): 
        if keys[pygame.K_UP] and y > vel:
            y -= vel

        if keys[pygame.K_DOWN] and y < 500 - height - vel:
            y += vel

        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        if jumpCount >= -10:
            neg = 1
            if jumpCount < 0:
                neg = -1
            y -= (7 ** 2) * 0.5 * neg
            jumpCount -= 1
        else: 
            jumpCount = 10
            isJump = False
        
    
    screen.fill((0,0,0))  # Fills the screen with black
    pygame.draw.rect(screen, (255,0,0), (x, y, width, height))
       
    pygame.display.update() 
    
pygame.quit()