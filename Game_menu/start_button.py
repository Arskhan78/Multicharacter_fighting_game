import pygame

# I used the following video to display an image. https://www.youtube.com/watch?v=G8MYGDf_9ho
# The start button button thing
class StartButton:
    def __init__(self, x: int, y: int, l: int, w: int, image: pygame.Surface, scale: float) -> None:
        ''' Defines the parameters that will be used in the class
        Args:
            x = Position on the x-axis
            y = Position on the y-axis
            l = Legnth of the rectangle
            w = Width of the rectangle
            image = .png or .jpg file
            scale = scale of the image
            text = string text
        Returns:
            None
        ''' 
        width = image.get_width()
        height = image.get_height()
        self.rect = pygame.Rect(x, y, l, w)
        self.x = x
        self.y = y
        self.l = l
        self.w = w
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
    
    def event_handling(self, event: pygame.event) -> None:
        """ Handles all the events for the button
        
        Args:
            event: Right click
        Returns:
            None
        """
        # Checks to see if the mouse is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                self.clicked = True
    
    def draw(self, surface: pygame.Surface) -> None:
        """ Displays the button
        Args:
            surface: screen
        Returns:
            None
        """
        # Retrives the position of the mouse
        pos = pygame.mouse.get_pos()

        # Different conditions for whether the button is being hovered over or not
        if self.rect.collidepoint(pos):
            surface.blit(self.image, (self.rect.x, self.rect.y + 10))
        else:
            surface.blit(self.image, (self.rect.x, self.rect.y))
