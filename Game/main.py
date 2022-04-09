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
    def __init__(self, name, hp, atk, speed, hitbox): #stamina
        self.name: str = name
        self.hp: int = hp
        self.atk: int = atk
        self.speed: int = speed
        self.hitbox: int = hitbox
        #self.stamina: int = stamina



    

    


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

    """
    Function determining how much dmg character recieved from other and vise versa
    Returns the other character hp - atk of the current character who called the function
    """
    def givedmg(self, otherchar:CharacterInstance):
        otherchar.character.hp -= CharacterStats.atk
        # Ex: Enemy 100 Hp - Character 20 Atk : Enemy 80 Hp left

    """
    attack right function
    draws a rectangle to show the attack's hitbox (to the right)
    """
    def attackright(self):
        if self.cantatk == False:
            i = 0
            posx = CharacterPhysics.rectx
            posy = CharacterPhysics.recty
            chareach = (CharacterPhysics.rectx + self.reachx + 10, CharacterPhysics.recty - self.reachy + 5)
            while i < 2:
                i += 1
                pygame.draw.rect(screen, (0, 0, 200), (CharacterPhysics.rectx + 10, CharacterPhysics.recty + 5, self.reachx, self.reachy))
            #reseting the screen so atk does not stay on screen    
            pygame.draw.rect(screen, (0, 0, 200), ( posx, posy, 0, 0))
        #if cantatk = True then pass the fucntion as character on cooldown
        else:
            pass
    
    """
    attack left function
    draws a rectangle to show the attack's hitbox (to the left)
    """
    def attackleft(self):
        if self.cantatk == False:
            i = 0
            posx = CharacterPhysics.rectx
            posy = CharacterPhysics.recty
            self.chareachx = CharacterPhysics.rectx - self.reachx - 10
            self.chareachy = CharacterPhysics.recty - self.reachy + 5
            while i < 2:
                i += 1
                pygame.draw.rect(screen, (0, 0, 200), (CharacterPhysics.rectx - 10, CharacterPhysics.recty + 5, self.reachx, self.reachy))
            #reseting the screen so atk does not stay on screen    
            pygame.draw.rect(screen, (0, 0, 200), ( posx, posy, 0, 0))
        #if cantatk = True then pass the function as character on cooldown
        else:
            pass

    """
    Function to tell computer that character attacked
    returns if attack as "true"
    """
    def attacked(self):
        if self.cantatk == False:
            self.ifatk == True
        else:
            self.ifatk == False

    
    """
    Function representing the cooldown before a characters next attack
    returns cantatk as "true" if ifatk is "true"
    """
    def cooldown(self):
        if self.ifatk == True:
            i = 0
            while i < self.cd:
                i += 1
                self.cantatk == True
            
            self.cantatk == False
        else:
            pass



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
        if self.useskill == False:
            travelled = CharacterPhysics.rectx - self.dis
            while CharacterPhysics.rectx > travelled:
                #character's x pos moving towards the left until it reaches the travelled distance
                CharacterPhysics.rectx -= self.dsp
                l = 0
                while l < self.scd:
                    l += 1
                    self.useskill == True
                    #else func determines that if the skill is "True" then it will skip and no action will occur
                else:
                    return f"Skill is on cooldown right now for {l} more seconds"
        else:
            pass

    """
    Character Skill (Part 2) "Dash Right"
    """
    def dashright(self):
        if self.useskill == False:
            travelled = CharacterPhysics.rectx + self.dis
            while CharacterPhysics.rectx < travelled:
                #character's x pos moving towards the right until it reaches the travelled distance
                CharacterPhysics.rectx += self.dsp
                l = 0
                while l < self.scd:
                    l += 1
                    self.useskill == True
                    #else func determines that if the skill is "True" then it will skip and no action will occur
                else:
                    pass
        else:
            return f"Skill is on cooldown right now for {l} more seconds"

    """
    Character Skill "Ground Slam"
    """
    def slam(self, otherchar:CharacterInstance):
        if self.useskill == False:
            while CharacterPhysics.recty >= "tile":
                CharacterPhysics.recty -= self.grav
            leftside = CharacterPhysics.rectx - self.area - 2
            rightside = CharacterPhysics.rectx + self.area
            up = CharacterPhysics.recty - self.height - 5
            if "Character interacts with floor":
                if otherchar.currentX in range(leftside, rightside) and otherchar.currentY in range(up):
                    otherchar.character.hp -= CharacterStats.atk
                    
                else:
                    pass
            l = 0
            while l < self.scd:
                l += 1
                self.useskill == True
                #else func determines that if the skill is "True" then it will skip and no action will occur
            else:
                return f"Skill is on cooldown right now for {l} more seconds"

class CharacterPhysics():
    """
    Charecter movement and tile collision 
    """
    def init(self, x, y):
        self.images_right = []
        self.index = 0 
        self.counter = 0
        player_surf = pygame.image.load(f'player_stance1.png').convert_alpha()
        self.image = pygame.transform.scale(player_surf, (50, 100))
        self.rect = self.image.get_rect()
        self.rectx = x 
        self.recty = y 
        self.vel_y = 0 
        self.jumped = False

    def bindings(self, left, right, up): 
        speedx = 0
        speedy = 0
        speed = 10
        left_border = 0
        right_border = 1160
        keys = pygame.key.get_pressed()
        if keys[left] and self.rectx >= left_border:
            speedx -= speed
            print(self.rect.x)
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
        self.rectx += speedx
        self.recty += speedy

        if self.rect.bottom > 675:
            self.rect.bottom = 675
            speedy = 0

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

    #player basic attack
    bplayer1 = BasicAttack(30, False, 5, 10, False)
    bplayer2 = BasicAttack(30, False, 5, 10, False)

    #player skill attack
    splayer1 = SkillAttack(5, 10, 20, 10, 40, False, 5)
    splayer2 = SkillAttack(5, 10, 20, 10, 40, False, 5)

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
                if event.key == K_r and K_RIGHT:
                    bplayer1.attackright()
                    if CharacterPhysics.rect.x + 10 <= bplayer1.chareachx and bplayer1.chareachy in range(CharacterPhysics.rect.y, CharacterPhysics.rect.y + 20):
                        bplayer1.givedmg()
                    else:
                        pass
                if event.key == K_r and K_LEFT:
                    bplayer1.attackleft()
                    if CharacterPhysics.rect.x <= bplayer1.chareachx and bplayer1.chareachy in range(CharacterPhysics.rect.y, CharacterPhysics.rect.y + 20):
                        bplayer1.givedmg()
                    else:
                        pass
                    bplayer1.attacked()
                    bplayer1.cooldown()

                elif event.key == K_m and K_RIGHT:
                    bplayer2.attackright()
                    if CharacterPhysics.rect.x + 10 <= bplayer2.chareachx and bplayer2.chareachy in range(CharacterPhysics.rect.y, CharacterPhysics.rect.y + 20):
                        bplayer2.givedmg()
                    else:
                        pass
                    bplayer2.attacked()
                    bplayer2.cooldown()
                elif event.key == K_m and K_LEFT:
                    bplayer2.attackleft()
                    if CharacterPhysics.rect.x <= bplayer2.chareachx and bplayer2.chareachy in range(CharacterPhysics.rect.y, CharacterPhysics.rect.y + 20):
                        bplayer2.givedmg()
                    else:
                        pass
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

        characterPhysics1.draw()
        characterPhysics1.bindings(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP)

        characterPhysics2.bindings(pygame.K_a, pygame.K_d, pygame.K_w)
        characterPhysics2.draw()
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        # --- Limit to 60 frames per second
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    main()