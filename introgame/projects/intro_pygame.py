
import pygame 
from sys import exit
from random import randint
from pygame import surface
from pygame import display
from pygame.constants import HIDDEN 

#RBG colors
rgb_grey = (64,64,64)
rgb_lightblue = (104,188,223) 
rgb_red = (245, 41, 41)
rgb_menublue = (51, 255, 255)

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time 
    score_surf = font.render(f'Score: {current_time}', False, rgb_grey)
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf, score_rect)
    return current_time

pygame.init()

clock = pygame.time.Clock()
game_active = False   
start_time = 0

width = 800
height = 400
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Runner') 


#Scoreboard
font = pygame.font.Font('assets/font/pixelfont.ttf', 50)
score = 0 
#score_surf = font.render('Score',False, rgb_grey)
#score_rect = score_surf.get_rect(center = (400,50))


#backround
#normally you want to convert png so use .convert(), if the png has extra coler pixers use .convert_alpa()
sky_surface = pygame.image.load('assets/graphics/Sky.png').convert()
ground_surface = pygame.image.load('assets/graphics/ground.png').convert()

#entities 
#snail
snail_surf = pygame.image.load('assets/playermodels/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(midbottom = (600,300))

#obstacles
obstacle_rect_list = []
#player
player_surf = pygame.image.load('assets/playermodels/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80,300))
#for intro screen
player_stand = pygame.image.load('assets/playermodels/player_stand.png').convert_alpha() 
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400,200))
#player gravity
player_gravity = 0 

#menu 
game_name = font.render('Ice Runner', False, rgb_menublue)
game_name_rect = game_name.get_rect(center =(400,80)) 

game_message = font.render('Press space to run', False, rgb_menublue)
game_message_rect = game_message.get_rect(center = (400, 340)) 

#timer 
obstacle_timer = pygame.USEREVENT + 1  #alsys do for this always add the +1
pygame.time.set_timer(obstacle_timer,900)  

while True:
    snail_rect = snail_surf.get_rect(midbottom = (600,300))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
           
        if game_active:
            #mouse button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300: 
                    player_gravity = -20
            #jumping  
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
        else: 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True 
                snail_rect.left = 800
                #for timer
                start_time = int(pygame.time.get_ticks() / 1000)
        #snail 
        # if event.type == obstacle_timer and game_active:
        #     obstacle_rect_list.append(snail_surf.get_rect(midbottom = (randint(900,1100,300)))

    #code for game    
    if game_active:
        #main area
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface,(0,300))
        #scoreboard
        #pygame.draw.rect(screen, rgb_lightblue, score_rect)
        #pygame.draw.rect(screen, rgb_lightblue, score_rect, 10)
        #screen.blit(score_surf,score_rect)
        score = display_score()

        #moving snail
        # snail_rect.x -= 4
        # if snail_rect.right <= 0: snail_rect.left = 800
        # screen.blit(snail_surf, snail_rect)

        #player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300: player_rect.bottom = 300
        screen.blit(player_surf,player_rect)
        
        #collision 
        if snail_rect.colliderect(player_rect):
            game_active = False
    #menu screens(startup and loss)
    else: 
        screen.fill(rgb_lightblue)
        screen.blit(player_stand, player_stand_rect) 
        screen.blit(game_name,game_name_rect)
        
        #to display score
        score_message = font.render(f'Your score: {score}', False, rgb_menublue)
        score_message_rect = score_message.get_rect(center = (400, 330))
        if score == 0: screen.blit(game_message,game_message_rect)
        else: screen.blit(score_message, score_message_rect)
        
        

    
    
    pygame.display.update()
    clock.tick(60)

