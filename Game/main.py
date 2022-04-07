import os
from xmlrpc.client import boolean
from numpy import block
import pygame
import ui
from typing import List, Tuple, Dict, Optional
import json
pygame.init()


size = (1200, 900)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("TEMPLATE")

blockTypes = ["air", "solid"]

class Simulation: 
    """
    A class for each game
    """
    def __init__(self, gridInt, player1, player2):
        grid = []
        for i in range(len(gridInt)):
            row = []
            for k in range(len(gridInt[0])):
                row.append(Blocks(k, i, blockTypes[gridInt[i][k]]))
            grid.append(row)
        self.grid: List[Blocks] = grid
        print(grid)
        self.player1: PlayerInstance = player1
        self.player2: PlayerInstance = player2

        #separated to allow for hard coding the spawn points, change later
        self.character1: CharacterInstance = CharacterInstance(player1.character, 20, 20)
        self.character2: CharacterInstance = CharacterInstance(player1.character, 90, 20)
    
    def tick(self):
        # physics stuff goes here
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

    """
    Function determining how much dmg character recieved from other
    """
    def recievedmg(self, otherchar:CharacterInstance):
        self.hp -= otherchar.character.atk
        pass

class BasicAttack:
    """
    Represents a character's basic attack
    """
    def __init__(self, cd, ifatk, range, cantatk):
        self.cd: int = cd
        self.ifatk: bool = ifatk
        self.range: int = range
        self.cantatk: bool = cantatk
        pass

    """
    Function to tell computer that character attacked
    """
    def attacked(self, ifatk, cantatk):
        if cantatk == False:
            ifatk == True
        else:
            ifatk == False

    
    """
    Function representing the cooldown before a characters next attack
    """
    def cooldown(self, ifatk, cd, cantatk):
        if ifatk == True:
            while cd < 30:
                cd += 1
                cantatk == True
            
            cantatk == False



class SkillAttack:
    """
    Represents a character's skill attack
    """
    def __init__(self, dis, grav, area):
        self.dis: int = dis
        self.grav: int = grav
        self.area: int = area
        pass

    """
    Character Skill "Dash Left"
    """
    def dashleft(self, dis):
        CharacterInstance.currentX -= dis

    """
    Character Skill (Part 2) "Dash Right"
    """
    def dashright(self, dis):
        CharacterInstance.currentX += dis

    """
    Character Skill "Ground Slam"
    """
    def slam(self, grav, otherchar:CharacterInstance, distance, area):
        y -= grav
        leftside = CharacterInstance.currentX - area
        rightside = CharacterInstance.currentX + area
        if "Character interacts with floor":
            if otherchar.currentX in range(leftside, rightside):
                "Interact function (Character is hit)"


        pass

        

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
    player1 = PlayerInstance("asd", 1, characters['bob'])
    player2 = PlayerInstance("asdd", 1, characters['bob'])
    sim = Simulation(maps['smash'], player1, player2)

    fpsCount = 0

    blockWidth = min(size[0]/len(sim.grid[0]), size[1]/len(sim.grid))
    print(blockWidth)

    while True:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        sim.tick() # <-- DO ALL PHYSICS PROCESSING IN HERE



        # temp rendering, scuffed af
        for i in range(len(sim.grid)):
            for k in range(len(sim.grid[0])):
                if sim.grid[i][k].type == "air":
                    pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(blockWidth*k, blockWidth*i, blockWidth, blockWidth))
                elif sim.grid[i][k].type == "solid":
                    pygame.draw.rect(screen, (153, 51, 0), pygame.Rect(blockWidth*k, blockWidth*i, blockWidth, blockWidth))
        
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(sim.character1.currentX/10*blockWidth, sim.character1.currentY/10*blockWidth, sim.character1.character.hitbox[0]/10*blockWidth, sim.character1.character.hitbox[1]/10*blockWidth))
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(sim.character2.currentX/10*blockWidth, sim.character2.currentY/10*blockWidth, sim.character2.character.hitbox[0]/10*blockWidth, sim.character2.character.hitbox[1]/10*blockWidth))
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
    
        # --- Limit to 60 frames per second
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    main()