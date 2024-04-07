import pygame

from pygame.sprite import Sprite

class Alien(Sprite):
    """Class to represent a single alien in fleet"""

    def __init__(self, ai_game, explosion_images, is_special=False):
        """Initialize alien and set starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load alien image and set rect attribute
        self.image = pygame.image.load('alien_invasion/images/alien.bmp')
        original_width, original_height = self.image.get_size()
        new_width = original_width // 5
        new_height = original_height // 5
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

        self.rect = self.image.get_rect()

        # Start each new alien near top left of screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store aliens horizontal position
        self.x = float(self.rect.x)

        # Explosion animation attributes
        self.explosion_images = []
        self.explosion_frame_index = 0
        self.explosion_speed = 5
        self.is_exploding = True 

        self.is_special = is_special

    def check_edges(self):
        """Return True if alien has reached edge of screen"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        """Move the alien horizontally"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x


    def explode(self):
        """Trigger explosion animation"""
        self.is_exploding = True

    def animate_explosion(self):
        """Animate explosion frames"""
        explosion_frame = self.explosion_images[self.explosion_frame_index]
        self.screen.blit(explosion_frame, self.rect)

        #Increment frame index
        self.explosion_frame_index += 1

        #Check if animation is complete and reset if needed
        if self.explosion_frame_index >= len(self.explosion_images):
            self.reset_explosion_animation()

    def reset_explosion_animation(self):
        """Reset explosion animation"""
        self.is_exploding = False
        self.explosion_frame_index = 0

    def draw(self):
        """Draw the alien on the screen"""
        self.screen.blit(self.image, self.rect)


        