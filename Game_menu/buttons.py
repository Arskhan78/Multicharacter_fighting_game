import pygame

# Activate pygame library and grant premission to use pygame's functionality
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Assigning the length and width of the screen and display the surface object
X = 800
Y = 500
screen = pygame.display.set_mode((X, Y))

# Set the caption of the game
pygame.display.set_caption('Fighting Game')

#load the image of the start button
start_img = pygame.image.load('start_btn.png').convert_alpha()

# Identify the arial font and assign it to the variable arial
arial = pygame.font.SysFont('arial', 25)
arial_2 = pygame.font.SysFont('arial', 35)

# Defining the RGB values of Black, Grey, and White
BLACK = (0, 0, 0)
GREY = (150, 150, 150)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# irrelavant
text = arial_2.render('Fighting Game', True, RED)
textRect = text.get_rect()
textRect.center = (X - 400, Y - 430)

# Input button class
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
 
# Main function
def main():

    button1 = clickButton(290, 295, 250, 40, start_img, 0.8, 'Start')
    username_2 = inputBox(275, 175, 250, 40, 'Username_2')
    username = inputBox(275, 115, 250, 40, 'Username')
    number_of_lives = inputBox(275, 235, 250, 40, 'Number of Lives')
    

    while True:
        # important
        screen.fill((202, 228, 241))
        screen.blit(text, textRect)
        # Will shut down the screen when the x button is clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            # Activate interaction abilities of all objects
            button1.eventHandling(event)

            username.eventHandling(event)

            number_of_lives.eventHandling(event)

            username_2.eventHandling(event)

        # Displays the start image and all other defined objects
        button1.draw(screen)
        username.draw()
        number_of_lives.draw()
        username_2.draw()

        # Will print the text inside each inputbox once the start button is clicked
        if button1.clicked:
            print(username.text)
            print(username_2.text)
            print(number_of_lives.text)

        button1.clicked = False



        # Updates the screen with the given parameters
        pygame.display.flip()
    
        # Limits FPS to 60
        pygame.time.Clock().tick(60)

        # Draws the surface object to the screen
        pygame.display.update()

# WIll run the main function if it is located on the same file as the function main

if __name__ == "__main__":
    main()
