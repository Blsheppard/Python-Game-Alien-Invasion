import pygame
import os

# Initialize Pygame
pygame.init()
print("Pygame initialized successfully.")

class ExplosionAnimation:
    def __init__(self, screen, explosion_images):
        self.screen = screen
        self.explosion_images = explosion_images
        self.explosion_frame_index = 0
        self.explosion_speed = 10
        self.is_exploding = False

    def animate_explosion(self, rect):
        """Animate explosion frames"""
        if self.is_exploding:
            explosion_frame = self.explosion_images[self.explosion_frame_index]
            self.screen.blit(explosion_frame, rect)

            # Increment frame index
            self.explosion_frame_index += 1

            # Check if animation is complete and reset if needed
            if self.explosion_frame_index >= len(self.explosion_images):
                self.reset_explosion_animation()

    def reset_explosion_animation(self):
        """Reset explosion animation"""
        self.is_exploding = False
        self.explosion_frame_index = 0

# Set up screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Explosion Animation")

# Load explosion images
explosion_images = []
explosion_folder = 'C:/Users/Shepp/OneDrive/Desktop/python_projects/alien_invasion/images/explosion_images/'
for i in range(1, 31):
    image_path = os.path.join(explosion_folder, f'explosion_images_{i}.png')
    explosion_images.append(pygame.image.load(image_path))

# Create an instance of ExplosionAnimation
explosion_animation = ExplosionAnimation(screen, explosion_images)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill screen with black
    screen.fill((0, 0, 0))

    # Animate the explosion at a specific position
    alien_rect = pygame.Rect(200, 200, 100, 100)
    explosion_animation.is_exploding = True  # Start the explosion animation
    explosion_animation.animate_explosion(alien_rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()

