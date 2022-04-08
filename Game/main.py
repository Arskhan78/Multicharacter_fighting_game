import os
import pygame
import ui
from typing import List, Tuple, Dict, Optional
import json
from pygame.locals import K_m, K_r, K_t, K_l, K_f, K_a, K_d, K_RIGHT, K_LEFT, K_PERIOD, KEYDOWN 
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
    def __init__(self, name, hp, atk, speed, hitbox, cd, ifatk, reach, cantatk, dis, grav, area, height, scd, useskill, dsp): #stamina
        self.name: str = name
        self.hp: int = hp
        self.atk: int = atk
        self.speed: int = speed
        self.hitbox: int = hitbox
        self.attack = BasicAttack(cd, ifatk, reach, cantatk)
        self.skill = SkillAttack(dis, grav, area, height, scd, useskill, dsp)
        #self.stamina: int = stamina
        pass


    """
    Function determining how much dmg character recieved from other and vise versa
    """
    def givedmg(self, otherchar:CharacterInstance):
        otherchar.character.hp -= self.atk

    

    


class BasicAttack:
    """
    Represents a character's basic attack
    """
    def __init__(self, cd, ifatk, reach, cantatk):
        self.cd: int = cd
        self.ifatk: bool = ifatk
        self.reach: int = reach
        self.cantatk: bool = cantatk
        

    def attack(self):
        if self.cantatk == False:
            i = 0
            while i < 2:
                pygame.draw.rect(screen, (0, 0, 200), (CharacterInstance.currentX, CharacterInstance.currentY, self.reach, self.reach))
            #reseting the screen so atk does not stay on screen    
            pygame.draw.rect(screen, (0, 0, 200), (CharacterInstance.currentX, CharacterInstance.currentY, 0, 0))
        #if cantatk = True then pass the fucntion as character on cooldown
        else:
            pass


    """
    Function to tell computer that character attacked
    """
    def attacked(self):
        if self.cantatk == False:
            self.ifatk == True
        else:
            self.ifatk == False

    
    """
    Function representing the cooldown before a characters next attack
    """
    def cooldown(self):
        if self.ifatk == True:
            i = 0
            while i < self.cd:
                i += 1
                self.cantatk == True
            
            self.cantatk == False



class SkillAttack:
    """
    Represents a character's skill attack
    """
    def __init__(self, dis, grav, area, height, scd, useskill, dsp):
        self.dis: int = dis
        self.grav: int = grav
        self.area: int = area
        self.height: int = height
        self.scd: int = scd
        self.useskill: bool = useskill
        self.dsp: int = dsp


    """
    Character Skill "Dash Left"
    """
    def dashleft(self,):
        travelled = CharacterInstance.currentX - self.dis
        while CharacterInstance.currentX > travelled:
            CharacterInstance.currentX -= self.dsp

    """
    Character Skill (Part 2) "Dash Right"
    """
    def dashright(self):
        travelled = CharacterInstance.currentX + self.dis
        while CharacterInstance.currentX < travelled:
            CharacterInstance.currentX += self.dsp

    """
    Character Skill "Ground Slam"
    """
    def slam(self, otherchar:CharacterInstance):
        if self.useskill == False:
            while CharacterInstance.currentY >= "tile":
                CharacterInstance.currentY -= self.grav
            leftside = CharacterInstance.currentX - self.area - 2
            rightside = CharacterInstance.currentX + self.area
            up = CharacterInstance.currentY + self.height
            if "Character interacts with floor":
                if otherchar.currentX in range(leftside, rightside) and otherchar.currentY in range(up):
                    otherchar.character.hp -= CharacterStats.atk
                    l = 0
                    while l < self.scd:
                        l += 1
                        self.useskill == True
                #else func determines that if the skill is "True" then it will skip and no action will occur
                else:
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

    #player basic attack
    bplayer1 = BasicAttack()
    bplayer2 = BasicAttack()

    #player skill attack
    splayer1 = SkillAttack()
    splayer2 = SkillAttack()

    fpsCount = 0

    blockWidth = min(size[0]/len(sim.grid[0]), size[1]/len(sim.grid))
    print(blockWidth)

    while True:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == KEYDOWN:
                #Basic Attack
                if event.key == K_r:
                    bplayer1.attack()
                    """
                    if hitbox in range:
                        bplayer2.givedmg()
                    else:
                        pass
                    """
                    bplayer1.attacked()
                    bplayer1.cooldown()

                elif event.key == K_m:
                    bplayer2.attack()
                    """
                    if hitbox in range:
                        bplayer2.givedmg()
                    else:
                        pass
                    """
                    bplayer2.attacked()
                    bplayer2.cooldown()

                #Abilties (Dash)
                elif event.key == K_t and K_a:
                    splayer1.dashleft()
                elif event.key == K_t and K_d:
                    splayer1.dashright()
                elif event.key == K_PERIOD and K_LEFT:
                    splayer2.dashleft()
                elif event.key == K_PERIOD and K_RIGHT:
                    splayer2.dashright()

                #Abilties (Slam)
                elif event.key == K_f:
                    splayer1.slam()
                elif event.key == K_l:
                    splayer2.slam()
            

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