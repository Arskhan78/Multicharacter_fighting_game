import pygame
from start_button import StartButton
from input_button import InputBox

''' Sources:
https://www.geeksforgeeks.org/how-to-create-a-text-input-box-with-pygame/
https://www.youtube.com/watch?v=G8MYGDf_9ho
https://www.geeksforgeeks.org/python-display-text-to-pygame-window/
https://www.youtube.com/watch?v=Rvcyf4HsWiw
https://www.pygame.org/docs/

'''

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
start_img = pygame.image.load('Start-Button-Vector-PNG.png').convert_alpha()

# Identify the arial font and assign it to the variable arial
arial = pygame.font.SysFont('arial', 25)
arial_2 = pygame.font.SysFont('arial', 35)

# Defining the RGB value of red
Red = (255, 0, 0)

# I used the following link to display a title in pygame. https://www.geeksforgeeks.org/python-display-text-to-pygame-window/
# Code for displaying a title in pygame
text = arial_2.render('Fighting Game', True, Red)
textRect = text.get_rect()
textRect.center = (X - 400, Y - 430)

# Main function
def main() -> None:
    ''' Incorporates the inputBox and clickButton classes while drawing a window
    Returns:
        No tangible value. Displays the screen while employing the two imported classes
    '''
    # Specifications of the button and the inputboxes that will be used
    button1 = StartButton(280, 285, 250, 40, start_img, 0.3)
    username_2 = InputBox(275, 175, 250, 40, 'Username_2')
    username = InputBox(275, 115, 250, 40, 'Username_1')
    number_of_lives = InputBox(275, 235, 250, 40, 'Number of Lives')
    
    # Main loop
    while True:
        # Colour of the screen acording to RGB values
        screen.fill((2, 2, 250))
        # Displays the main title
        screen.blit(text, textRect)
        # Will shut down the screen when the x button is clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            # Activate interaction abilities of all objects
            button1.event_handling(event)

            username.event_handling(event)

            number_of_lives.event_handling(event)

            username_2.event_handling(event)

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
            exit()

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
