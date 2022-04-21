from random import random
from re import L
from tkinter import Grid
from turtle import up
from numpy import block
import pygame
import random

pygame.init()


size = (1200, 900)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("TEMPLATE")

blockTypes = ["air", "solid"]

class CharacterPhysics:  #http://codingwithruss.com/pygame/platformer/player.html i got jumping code from here (modified) https://www.youtube.com/watch?v=MYaxPa_eZS0&t=760s for sprite logic (modified)
    """
    Charecter movement and tile collision 
    """
    def __init__(self, x, y):
        self.sprites = []
        self.sprites.append(pygame.image.load('charactersprites/Idle__000.png'))
        self.sprites.append(pygame.image.load('charactersprites/Idle__001.png'))
        self.sprites.append(pygame.image.load('charactersprites/Idle__002.png'))
        self.sprites.append(pygame.image.load('charactersprites/Idle__003.png'))
        self.sprites.append(pygame.image.load('charactersprites/Idle__004.png'))
        self.sprites.append(pygame.image.load('charactersprites/Idle__005.png'))
        self.sprites.append(pygame.image.load('charactersprites/Idle__006.png'))
        self.sprites.append(pygame.image.load('charactersprites/Idle__007.png'))
        self.sprites.append(pygame.image.load('charactersprites/Idle__008.png'))
        self.sprites.append(pygame.image.load('charactersprites/Idle__009.png'))
        self.animationcycle = 0
        self.idle = False
        player_surf = self.sprites[self.animationcycle].convert_alpha()
        self.image = pygame.transform.scale(player_surf, (50, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y 
        self.vel_y = 0 
        self.jumped = False

    def collision(self, grid, blockWidth):
        corners = [[self.rect.top, self.rect.left], [self.rect.top, self.rect.right], [self.rect.bottom, self.rect.left], [self.rect.bottom, self.rect.right]]
        cornerCollisions = [False, False, False, False]
        for i in range(len(grid)):
            for k in range(len(grid[0])):
                if grid[i][k].type == 'solid':
                    print(i, k)
                    for c in range(len(corners)):
                        if corners[c][0] >= i*blockWidth and corners[c][0] <= (i+1)*blockWidth and corners[c][1] >= k*blockWidth and corners[c][1] <= (k+1)*blockWidth:
                            cornerCollisions[c] = True
        ret = {
            'left': cornerCollisions[0] and cornerCollisions[2],
            'right': cornerCollisions[1] and cornerCollisions[3],
            'bottom': cornerCollisions[2] or cornerCollisions[3],
            'top': cornerCollisions[0] or cornerCollisions[1]
        }
        print(ret)
        return ret
    
    def animation_idle(self): 
        self.idle = True
    
    def bindings(self, left, right, up, grid, bw): #how to we display this in uml (go to main on line 155/157)
        collisions = self.collision(grid, bw)
        speedx = 0
        speedy = 0
        speed = 15
        left_border = 0
        right_border = 1160
        keys = pygame.key.get_pressed()
        if keys[left] and self.rect.x >= left_border:
            speedx -= speed
            self.animation_idle()
            print(self.rect.x)
        if keys[right] and self.rect.x <= right_border:
            speedx += speed
            print(self.rect.x)
        # jumping code starts here ---------------------------
        if keys[up] and self.jumped == False:
            self.vel_y = -25
            self.jumped = True
        # modified bit (i capped speed in air for both x directions)
        if keys[left] and self.jumped == True:
            speedx += 10
        if keys[right] and self.jumped == True :
            speedx -= 10
        # checking if jumped
        if  collisions['bottom']:
            self.jumped = False
       
        #gravity 
        self.vel_y += 1
        if self.vel_y > 15:
            self.vel_y = 15    

        speedy += self.vel_y

        if collisions['bottom']:
            speedy = min(0, speedy)

        if collisions['right']:
            speedx = min(0, speedx)
        
        if collisions['left']:
            speedx = max(0, speedx)

        if collisions['top']:
            speedy = max(0, speedy)
        
        if self.rect.y > 900: 
            self.rect.x = random.randrange(200, 700)
            self.rect.y = -200

        self.rect.x += speedx
        self.rect.y += speedy
    
    def animations(self):
        if self.idle == True:
            self.animationcycle += 0.3
            if self.animationcycle >= len(self.sprites):
                self.animationcycle = 0
                #self.idle = False                                          #for only 1 use

            # if self.bindings(right, up):
            #     self.idle == False
            player_surf = self.sprites[int(self.animationcycle)].convert_alpha()
            self.image = pygame.transform.scale(player_surf, (50, 100))

        

    def draw(self):
        screen.blit(self.image, self.rect)
