import pygame

# Activate pygame libraries and initiate pygame functionality
pygame.init()

# Defining the RGB values of black 
Black = (0, 0, 0)

# Identify the arial font and assign it to the variable arial
arial = pygame.font.SysFont('arial', 25)

# Assigning the length and width of the screen and display the surface object
X = 800
Y = 500
screen = pygame.display.set_mode((X, Y))

# I got some help from this website for making an inputbox ckass. https://www.geeksforgeeks.org/how-to-create-a-text-input-box-with-pygame/
# Inputbox class
class InputBox:
    def __init__(self, x: int, y: int, l: int, w: int, default_text: str) -> None:
        ''' Defines the parameters that will be used in the class
        Args:
            x = Position on the x-axis
            y = Position on the y-axis
            l = length of the object
            w = width of the object
            defaultText = String assigned to show to the user
        Returns:
            None. Will display an input box with the given parameters
        '''
        self.rect = pygame.Rect(x, y, l, w)
        self.x = x
        self.y = y
        self.l = l
        self.w = w
        self.default_text = default_text
        self.in_use = False
        self.text = ''

    def event_handling(self, event: pygame.event) -> None:
        """ handles all the events for the inputbox
        
        Args:
            events: Right click and typing
        
        Returns:
            None
        """
        # Determines whether the box has been clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                self.in_use = True
            else:
                self.in_use = False
        # Handles event for when the box is in use
        elif event.type == pygame.KEYDOWN and self.in_use:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
    
    def draw(self: None) -> None:
        """ Displays the inputbox
        """
        # Different conditions for when the box is being edited or not
        pygame.draw.rect(screen, Black, pygame.Rect(self.x, self.y, self.l, self.w), 5)
        if self.in_use or self.text:
            screen.blit(arial.render(self.text, False, Black), (self.x + 15, self.y + 5))
        else:
            screen.blit(arial.render(self.default_text, False, Black), (self.x + 15, self.y + 5))