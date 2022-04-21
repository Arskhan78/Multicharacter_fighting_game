from dis import pretty_flags
import os
from random import random
from tkinter import Grid
from numpy import block
import pygame
import ui
from typing import List, Tuple, Dict, Optional
import json
import math
import random
from class_1 import CharacterPhysics
from animations_method import import_folder
pygame.init()


size = (1200, 900)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("TEMPLATE")

blockTypes = ["air", "solid"]
Backround = pygame.image.load('NW0mK39.gif')
map_backround = pygame.transform.scale(Backround, (1200, 900))
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
        screen.blit(map_backround, (0,0)) 

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
        characterPhysics1.animations()
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