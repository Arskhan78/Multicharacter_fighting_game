from ctypes import resize
from turtle import left, right
import pygame, sys
from pygame.locals import *



pygame.init()
screen_width = 1200
screen_height = 800
screen_size = (screen_width, screen_height)
screen = pygame.display.set_mode((screen_width,screen_height), 0, 64)

display = pygame.Surface((600, 400))
pygame.display.set_caption('1v1 Fighting')
clock = pygame.time.Clock()

def universal(): #for global
    global player_y_speed
    global player1_location_x
    global player1_location_y
 

player1_image = pygame.image.load('assets/sprites/player/windplayer/wind_hashashin.png')
grass_image = pygame.image.load('assets/graphics/grass.png')
dirt_image = pygame.image.load('assets/graphics/dirt.png')
TILE_SIZE = grass_image.get_width()



# O = air
# 1 = dirt
# 2 = grass
game_map = [['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],  
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],   
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','2','2','2','2','2','2','2','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','2','2','2','2','2','2','0','2','2','2','2','2','2','0','0','0'],
            ['0','0','0','1','1','1','1','1','1','0','1','1','1','1','1','1','0','0','0'],
            ['0','0','0','1','1','1','1','1','1','0','1','1','1','1','1','1','0','0','0'],
            ['0','0','0','1','1','1','1','1','1','0','1','1','1','1','1','1','0','0','0'],
            ['0','0','0','1','1','1','1','1','1','0','1','1','1','1','1','1','0','0','0'],
            ['3','3','3','1','1','1','1','1','1','3','1','1','1','1','1','1','3','3','3']]


#colors
#backround_color = (204,255,255)
backround_color = (168, 245, 247)

moving_right = False
moving_left = False 

player1_location_x = 0
player1_location_y = 0
player1_location = (player1_location_x, player1_location_y )
player_y_speed = 0


player1_rect = pygame.Rect(player1_location_x, player1_location_y, player1_image.get_width(), player1_image.get_height())
contact_rect = pygame.Rect(200, 200, 200, 100)




def collision(rect, tiles):  #from da fluffy potatao YT https://www.youtube.com/watch?v=abH2MSBdnWc&list=PLX5fBCkxJmm1fPSqgn9gyR3qih8yYLvMj&index=3 14 min - 21 min
    contact_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            contact_list.append(tile)
    return contact_list



def movement(rect, movement, tiles):  #from da fluffy potatao YT https://www.youtube.com/watch?v=abH2MSBdnWc&list=PLX5fBCkxJmm1fPSqgn9gyR3qih8yYLvMj&index=3 14 min - 21 min
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types
    
    

def combo():
    pass

while True:
    display.fill(backround_color)

    #map configuaration
    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(dirt_image, (x * TILE_SIZE, y * TILE_SIZE))
            elif tile == '2':
                display.blit(grass_image, (x * TILE_SIZE, y * TILE_SIZE))
            elif tile != '0':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 2
        y += 2


   
    #moving the player
    player_movement_x = 0
    player_movement_y = 0
    player_movement = (player_movement_x, player_movement_y)
    if moving_right == True:
        player_movement_x += 4
    if moving_left == True:
        player_movement_x -= 4
    player_movement_x += player_y_speed
    player_y_speed += 0.4
    if player_y_speed > 6:
        player_y_speed = 6

        
    
    display.blit(player1_image,player1_location)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
                
    surf = pygame.transform.scale(display, screen_size)
    screen.blit(surf,(0,0))
    pygame.display.update()
    clock.tick(60)