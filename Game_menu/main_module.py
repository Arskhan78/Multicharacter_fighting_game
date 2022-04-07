import pygame
from click_button import clickButton
from input_button import inputBox

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

# Defining the RGB value of red
RED = (255, 0, 0)

# irrelavant
text = arial_2.render('Fighting Game', True, RED)
textRect = text.get_rect()
textRect.center = (X - 400, Y - 430)

# Main function
def main():

    button1 = clickButton(290, 295, 250, 40, start_img, 0.8, 'Start')
    username_2 = inputBox(275, 175, 250, 40, 'Username_2')
    username = inputBox(275, 115, 250, 40, 'Username_1')
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
