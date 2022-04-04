import pygame 
import sys
from pygame.locals import *
from game.tilesheet import Tilesheet


class Game:
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((1600, 800))
        self.clock = pygame.time.Clock()

        self.bg_coler = pygame.Color('black')

        self.tiles = Tilesheet('assets/platforms.png', 16, 16, 7, 14)


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
    
    def update(self):
        pass

    def draw(self):
        self.screen.fill (self.bg_coler)
        self.tiles.draw(self.screen)
        pygame.display.flip()