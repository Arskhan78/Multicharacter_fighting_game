import pygame
import button

#create display window
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Button Demo')

#load button images
start_img = pygame.image.load('start_button.jpg').convert_alpha()

#create button instances
start_button = button.Button(300, 210, start_img, 0.5)


#game loop
run = True
while run:

	screen.fill((202, 228, 241))

	if start_button.draw(screen):
		print('START')

	#event handler
	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()
