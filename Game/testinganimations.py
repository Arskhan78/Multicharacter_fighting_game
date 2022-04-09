
while i < 5:
    value += 1
    i += 1
                # Setting 0 in value variable if its
                # value is greater than the length
                # of our sprite list
    if value >= len(image_sprite):
        value = 0
            
                # Storing the sprite image in an
                # image variable
    image = image_sprite[value]
    image_flip = pygame.transform.flip(image, True, False)
                # Scaling the image
    image = pygame.transform.scale(image_flip, (self.reachx, self.reachy))
            
                # Displaying the image in our game window
    screen.blit(image_flip, (CharacterPhysics.rect.x + 10, CharacterPhysics.rect.y + 5))

while i < 5:
    i += 1
    value += 1
               # Setting 0 in value variable if its
                # value is greater than the length
                # of our sprite list
    if value >= len(image_sprite):
        value = 0
            
                # Storing the sprite image in an
                # image variable
    image = image_sprite[value]
            
                # Scaling the image
    image = pygame.transform.scale(image, (self.reachx, self.reachy))
            
                # Displaying the image in our game window
    screen.blit(image, (CharacterPhysics.rect.x + 10, CharacterPhysics.rect.y + 5))