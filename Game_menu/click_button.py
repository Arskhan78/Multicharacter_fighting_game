import pygame

# The start button button thing
class clickButton:
    def __init__(self, x, y, w, h, image, scale, text):
        ''' Defines the parameters that will be used in the class
        '''
        width = image.get_width()
        height = image.get_height()
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.text = text
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
    
    def eventHandling(self, event: pygame.event):
        """ Handles all the events for the button
        
        Args:
            event: Right click
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                self.clicked = True
    
    def draw(self, surface):
        """ Displays the button
        """
        pos = pygame.mouse.get_pos()

        # Different conditions for whether the button is being hovered over or not
        if self.rect.collidepoint(pos):
            # pygame.draw.rect(screen, WHITE, pygame.Rect(self.x, self.y, self.w, self.h))
            # screen.blit(arial.render(self.text, False, BLACK), (self.x + 15, self.y + 5))
            surface.blit(self.image, (self.rect.x, self.rect.y + 10))
        else:
            surface.blit(self.image, (self.rect.x, self.rect.y))
