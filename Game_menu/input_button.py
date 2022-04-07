import pygame

# Activate pygame libraries and initiate pygame functionality
pygame.init()

# Defining the RGB values of Black, Grey, and White
BLACK = (0, 0, 0)
GREY = (150, 150, 150)
WHITE = (255, 255, 255)

# Identify the arial font and assign it to the variable arial
arial = pygame.font.SysFont('arial', 25)

# Assigning the length and width of the screen and display the surface object
X = 800
Y = 500
screen = pygame.display.set_mode((X, Y))

# Inputbox class
class inputBox:
    def __init__(self, x, y, w, h, defaultText):
        ''' Defines the parameters that will be used in the class
        '''
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.defaultText = defaultText
        self.inUse = False
        self.text = ''

    def eventHandling(self, event: pygame.event):
        """ handles all the events for the inputbox
        
        Args:
            events: Right click and typing

        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                self.inUse = True
            else:
                self.inUse = False
        elif event.type == pygame.KEYDOWN and self.inUse:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
    
    def draw(self):
        """ Displays the inputbox
        """
        # Different conditions for when the box is being edited or not
        pygame.draw.rect(screen, BLACK, pygame.Rect(self.x, self.y, self.w, self.h), 5)
        if self.inUse or self.text:
            screen.blit(arial.render(self.text, False, BLACK), (self.x + 15, self.y + 5))
        else:
            screen.blit(arial.render(self.defaultText, False, BLACK), (self.x + 15, self.y + 5))
