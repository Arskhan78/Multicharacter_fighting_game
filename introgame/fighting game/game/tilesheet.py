import pygame

class Tilesheet:
    def __init__(self, filename, width, height, rows, collums):
        image = pygame.image.load(filename).convert()
        self.title_table = []
        for tile_x in range(0, collums): 
            line = []
            self.title_table.append(line)
            for tile_y in range (0, rows):
                rect = (tile_x * width, tile_y * height, width, height)
                line.append(image.subsurface(rect))

    def draw(self, screen): 
         for x, row in enumerate(self.title_table):
             for y, tile in enumerate(row):
                 screen.blit(tile, (x * 72, y *72))