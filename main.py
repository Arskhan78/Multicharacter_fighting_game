import os
from tkinter import Grid
from numpy import block
import pygame
import ui
from typing import List, Tuple, Dict, Optional
import json
import math

pygame.init()


size = (1200, 900)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("TEMPLATE")

blockTypes = ["air", "solid"]

class Simulation: 
    """
    A class for each game
    """
    def __init__(self, gridInt):
        grid = []
        for i in range(len(gridInt)):
            row = []
            for k in range(len(gridInt[0])):
                row.append(Blocks(k, i, blockTypes[gridInt[i][k]]))
            grid.append(row)
        self.grid: List[Blocks] = grid
        self.blockWidth = 0
        pass


class Blocks:
    """
    Blocks that are in the map
    """
    def __init__(self, x, y, type):
        self.x: float = x
        self.y: float = y
        self.type: str = type

class PlayerInstance:
    """
    A class for a player instance
    """
    def __init__(self, username, lives, character):
        self.username: str = username
        self.lives: int = lives
        self.character: CharacterStats = character
        pass

class CharacterInstance:
    """
    A class for when a character is spawned
    """
    def __init__(self, character, x, y):
        self.character: CharacterStats = character
        self.currentHp: int = character.hp
        self.currentX: int = x
        self.currentY: int = y

class CharacterStats:
    """
    The base stats, attacks, etc of a character
    """
    def __init__(self, name, hp, atk, speed, hitbox):
        self.name: str = name
        self.hp: int = hp
        self.atk: int = atk
        self.speed: int = speed
        self.hitbox: int = hitbox
        pass

class BasicAttack:
    """
    Represents a character's basic attack
    """
    def __init__(self):
        pass

class SkillAttack:
    """
    Represents a character's skill attack
    """
    def __init__(self):
        pass

class CharacterPhysics():  #http://codingwithruss.com/pygame/platformer/player.html i got jumping code from here and tile collision for the map (modified)
    """
    Charecter movement and tile collision 
    """
    def __init__(self, x, y):
        player_surf = pygame.image.load(f'player_stance1.png').convert_alpha()
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
    
    def bindings(self, left, right, up, grid, bw): 
        collisions = self.collision(grid, bw)
        speedx = 0
        speedy = 0
        speed = 10
        left_border = 0
        right_border = 1160
        keys = pygame.key.get_pressed()
        if keys[left] and self.rect.x >= left_border:
            speedx -= speed
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
            speedx += 5
        if keys[right] and self.jumped == True :
            speedx -= 5
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

        self.rect.x += speedx
        self.rect.y += speedy

        #collisions 
        # for tile in sim.grid:
        #     if tile[solid] 
        #     pass

    def draw(self):
        screen.blit(self.image, self.rect)
    
    pass

characterPhysics1 = CharacterPhysics(100,200)    
characterPhysics2 = CharacterPhysics(600,200)    



def main():

    # loading all maps
    maps = {}
    for dir in os.listdir('maps/'):
        with open(f"maps/{dir}", 'r') as f:
            map = json.load(f)
            maps[map['name']] = map['grid']
    print(maps)

    # loading all characters from /characters 
    characters = {}
    for dir in os.listdir('characters/'):
        with open(f"characters/{dir}", 'r') as f:
            char = json.load(f)
            characters[char['name']] = CharacterStats(**char)
    print(characters)
    
    # temp for testing
    global sim
    sim = Simulation(maps['smash'])

    #player
   

    fpsCount = 0

    blockWidth = min(size[0]/len(sim.grid[0]), size[1]/len(sim.grid))
    print(blockWidth)

    sim.blockWidth = blockWidth

    while True:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

      

        # temp rendering, scuffed af
        
        for i in range(len(sim.grid)):
            for k in range(len(sim.grid[0])):
                if sim.grid[i][k].type == "air":
                    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(blockWidth*k, blockWidth*i, blockWidth, blockWidth))
                elif sim.grid[i][k].type == "solid":
                    pygame.draw.rect(screen, (153, 51, 0), pygame.Rect(blockWidth*k, blockWidth*i, blockWidth, blockWidth),2)
     
        
        characterPhysics1.draw()
        characterPhysics1.bindings(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, sim.grid, sim.blockWidth)
        characterPhysics2.draw()
        characterPhysics2.bindings(pygame.K_a, pygame.K_d, pygame.K_w, sim.grid, sim.blockWidth)
       

        pygame.display.update()
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
    
        # --- Limit to 60 frames per second
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    main()