import os
import pygame
import ui
from typing import List, Tuple, Dict, Optional
import json
from pygame.locals import K_m, K_r, K_t, K_l, K_f, K_a, K_d, K_RIGHT, K_LEFT, K_PERIOD, KEYDOWN 
import random 
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
    def __init__(self, name, hp, atk, speed, hitbox, maxatk): #stamina
        self.name: str = name
        self.hp: int = hp
        self.atk: int = atk
        self.speed: int = speed
        self.hitbox: int = hitbox
        self.maxatk: int = maxatk
        self.curatk: int = self.atk
        #self.stamina: int = stamina

    def increasedmg(self, idmg: int) -> None:
        try:
            self.atk = min(self.atk + idmg, self.maxatk)
        except(SyntaxError):
            print("That is not a number!\n")
            self.atk = self.curatk


    def decreasedmg(self, ddmg: int) -> None:
        self.curatk = self.atk
        try:
            self.atk = max(self.atk - ddmg, 0)
        except(SyntaxError):
            print("That is not a number!\n")
            self.atk = self.curatk

    def changename(self, changed: str) -> None:
        self.name = changed

    def displaychanges(self):
        return f"Name changed to: {self.name} and attack changed to: {self.atk}"

class BasicAttack:
    """
    Represents a character's basic attack
    """
    def __init__(self, cd, ifatk, reachx, reachy, cantatk):
        self.cd: int = cd
        self.ifatk: bool = ifatk
        self.reachx: int = reachx
        self.reachy: int = reachy
        self.cantatk: bool = cantatk


    #attack bindings
    def abindings(self, left, right, attack, otherchar: CharacterInstance):
        keys = pygame.key.get_pressed()
        i = 0

        #left attack
        if keys[left] and keys[attack] and self.cantatk == False:
            posx = CharacterPhysics.rectx
            posy = CharacterPhysics.recty
            self.chareachx = CharacterPhysics.rectx + self.reachx - 10
            self.chareachy = CharacterPhysics.recty - self.reachy + 5
            while i < 2:
                i += 1
                pygame.draw.rect(screen, (0, 0, 200), (CharacterPhysics.rectx + 10, CharacterPhysics.recty + 5, self.reachx, self.reachy))
            #reseting the screen so atk does not stay on screen    
            pygame.draw.rect(screen, (0, 0, 200), ( posx, posy, 0, 0))
            if CharacterPhysics.rect.x <= self.chareachx and self.chareachy in range(CharacterPhysics.rect.y, CharacterPhysics.rect.y + 20):
                otherchar.character.hp -= CharacterStats.atk
            

        #right attack
        if keys[right] and keys[attack] and self.cantatk == False:
            posx = CharacterPhysics.rectx
            posy = CharacterPhysics.recty
            self.chareachx = CharacterPhysics.rectx + self.reachx + 10
            self.chareachy = CharacterPhysics.recty - self.reachy + 5
            while i < 2:
                i += 1
                pygame.draw.rect(screen, (0, 0, 200), (CharacterPhysics.rectx + 10, CharacterPhysics.recty + 5, self.reachx, self.reachy))
            #reseting the screen so atk does not stay on screen    
            pygame.draw.rect(screen, (0, 0, 200), ( posx, posy, 0, 0))
            if CharacterPhysics.rect.x <= self.chareachx and self.chareachy in range(CharacterPhysics.rect.y, CharacterPhysics.rect.y + 20):
                otherchar.character.hp -= CharacterStats.atk
            

        #cooldown
        if keys[attack]:
            # if can atk then will atk
            if self.cantatk == False:
                self.ifatk == True
            else:
                self.ifatk == False
            # cooldown for atk
            if self.ifatk == True:
                while i < self.cd:
                    i += 1
                self.cantatk == True       
            self.cantatk == False

basicAttack1 = BasicAttack(30, False, 5, 10, False)
basicAttack2 = BasicAttack(30, False, 5, 10, False)

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

    def sbindings(self, left, right, dash, slam, grid, bw, otherchar:CharacterInstance):
        collisions = CharacterPhysics.collision(self, grid, bw)
        keys = pygame.key.get_pressed()
        l = 0
        floor = False
        # dash left
        if keys[dash] and keys[left] and self.useskill == False:
            travelled = CharacterPhysics.rectx - self.dis
            while CharacterPhysics.rectx > travelled:
                CharacterPhysics.rectx -= self.dsp
            while l < self.scd:
                l += 1
                self.useskill == True
        # dash right
        if keys[dash] and keys[right] and self.useskill == False:
            travelled = CharacterPhysics.rectx + self.dis + 10
            while CharacterPhysics.rectx < travelled:
                CharacterPhysics.rectx += self.dsp
            while l < self.scd:
                l += 1
                self.useskill == True
        else:
            pass
        # slam
        if keys[slam] and self.useskill == False:
            while floor == False:
                CharacterPhysics.recty += self.grav
            leftside = CharacterPhysics.rectx - self.area
            rightside = CharacterPhysics.rectx + self.area + 5
            up = CharacterPhysics.recty - self.height - 5
            if collisions['bottom']:
                CharacterPhysics.recty = min(0, CharacterPhysics.recty)
                if CharacterPhysics.rectx in range(leftside, rightside) and CharacterPhysics.recty in range(up):
                    otherchar.character.hp -= CharacterStats.atk

            while l < self.scd:
                l += 1
                self.useskill == True

        
skillAttack1 = SkillAttack(5, 10, 20, 10, 40, False, 5)
skillAttack2 = SkillAttack(5, 10, 20, 10, 40, False, 5)

class CharacterPhysics:
    """
    Charecter movement and tile collision 
    """
    def init(self, x, y):
        player_surf = pygame.image.load(f'player_stance1.png').convert_alpha()
        self.image = pygame.transform.scale(player_surf, (50, 100))
        self.rect = self.image.get_rect()
        self.rectx: int = x 
        self.recty: int = y 
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
        if keys[left] and self.rectx >= left_border:
            speedx -= speed
            print(self.rectx)
        if keys[right] and self.rectx <= right_border:
            speedx += speed
            print(self.rectx)
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
        if keys[up] and self.rect.bottom == 675:
            self.jumped = False 
        if  self.rect.bottom == 675:
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

    def draw(self):
        screen.blit(self.rect)

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

        characterPhysics1.draw()
        characterPhysics1.bindings(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP)
        skillAttack1.sbindings(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_PERIOD, pygame.K_COMMA)
        basicAttack1.abindings(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_p)

        characterPhysics2.bindings(pygame.K_a, pygame.K_d, pygame.K_w)
        skillAttack2.sbindings(pygame.K_a, pygame.K_d, pygame.K_r, pygame.K_t)
        basicAttack2.abindings(pygame.K_a, pygame.K_d, pygame.K_g)
        characterPhysics2.draw()
        
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        # --- Limit to 60 frames per second
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    main()