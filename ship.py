import pygame

class Ship:
    """Class to manage ship"""

    def __init__(self, ai_game):
        """Initialize ship and set starting postion"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load ship image and get its rect.
        self.image = pygame.image.load('alien_invasion/images/ship.bmp')

        # Get the original width and height of the image
        original_width, original_height = self.image.get_size()

        # Calculate the new width and height (50% of the original dimensions)
        new_width = original_width // 3.5
        new_height = original_height // 3.5

        # Scale down the image using the new dimensions
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        
        self.rect = self.image.get_rect()

        # Start every new ship at bottom center of screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a new float for ships horizontal position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        # Movement flag: ship that's not moving
        self.moving_right = False
        self.moving_left =  False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update ship position based on movement flag"""
        # Update ships x value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        #Update rect position
        self.rect.y = self.y

        # Update rect object from self.x
        self.rect.x = self.x

    def blitme(self):
        """Draw ship at this location"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen"""
        self.rect.midbottom = self.screen.get_rect().midbottom
        self.x = float(self.rect.x)