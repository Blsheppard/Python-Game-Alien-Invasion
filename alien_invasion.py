import sys
import pygame
import time
import random
import os

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from leaderboard import Leaderboard

class AlienInvasion:
    """Overall class to manage game assests and behavior."""

    def __init__(self):
        """Initialize game and resources"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.lives = self.settings.initial_lives
        self.collision_detected = False
        self.game_started = False
        high_scores_file = os.path.join(os.path.dirname(__file__), "high_scores.txt")
        self.leaderboard = Leaderboard(high_scores_file)

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Load bullet sound
        self.bullet_sound = pygame.mixer.Sound("alien_invasion/sounds/mixkit-short-laser-gun-shot-1670.wav")

        self.explosion_images = []
        for i in range(1, 31):  
            image_path = f'C:/Users/Shepp/OneDrive/Desktop/python_projects/alien_invasion/images/explosion_images/explosion_images_{i}.png'
            self.explosion_images.append(pygame.image.load(image_path))

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        
        self._create_fleet()
        self.initial_fleet_size = len(self.aliens)
        self.respawn_count = 0

        # Define point value
        self.alien_point_value = 20
        self.special_alien_point_value = 100

        self.score = 0
        self.high_score = 0

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse events.
            if not self.game_started:
                self._start_screen()
            else:
                self._check_events()
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._check_collisions()
                self._check_aliens_bottom()
                self._check_ship_alien_collision()
                self._update_screen()
                self.clock.tick(45)
                self.collision_detected = False  # Reset collision flag at the end of the frame

            # Check if player has run out of lives
            if self.lives <= 0:
                self._end_game()
                break

    def _start_game(self):
        """Start game"""
        self.run_game()

    def _start_screen(self):
        """Display start screen"""
        self.screen.fill(self.settings.bg_color)  # Fill screen with background color
        font = pygame.font.Font(None, 36)
        text = font.render("Press ENTER to start game", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(text, text_rect)

        # Display action menu
        action_text = [
        "<- MOVE LEFT",
        "-> MOVE RIGHT",
        "^ MOVE FORWARD",
        "SPACEBAR TO SHOOT"
    ]
        for i, line in enumerate(action_text, start=1):
            action_render = font.render(line, True, (255, 255, 255))
            action_rect = action_render.get_rect(center=(text_rect.centerx, text_rect.centery + 50 * i))
            self.screen.blit(action_render, action_rect)
        pygame.display.flip()

        # Wait for player to press ENTER
        self._check_start_event()

    def _check_start_event(self):
        """Check for ENTER key press to start the game"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game_started = True
                    return

    def _check_collisions(self):
        """Check for collisions between game objects"""
        self._check_bullet_alien_collisions()
        self._check_ship_alien_collision()
                    
    def _check_events(self):
        """Respond to keypresses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self._start_game()
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to key presses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True

    def _check_keyup_events(self, event):
        """Respond to key release"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """Create new bullet and add it to bullet group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.bullet_sound.play( )

    def _update_bullets(self):
        """Update position of bullet and get rid of old bullets"""
        #Update bullet position
        self.bullets.update()
        
        #Get rid of old bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # Destroy existing bullets and create new fleet of aliens
        self._check_bullet_alien_collisions()
            
    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collision"""
        # Remove any bullets and aliens that have collided
        collision = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        for aliens_hit in collision.values():
            for alien in aliens_hit:
                if alien.is_special:
                    self.score += self.special_alien_point_value
                else:
                    self.score += self.alien_point_value

                # Update high score if needed
                if self.score > self.high_score:
                    self.high_score = self.score
                
        if not self.aliens:
            # Destroy existing bullets and create new fleet
            start_time = time.time()
            while time.time() - start_time < 2:
                pygame.display.update()
            # Create a new fleet of aliens after the delay
            self._create_fleet()
            self._increase_difficulty()
        
    def _increase_difficulty(self):
        """Increase speed and difficulty"""
        # Create a new fleet of aliens before increasing the difficulty
        self._create_fleet()

        # Increase speed and other difficulty parameters
        self.settings.alien_speed *= 1.2  # Increase alien speed by 10%
        self.settings.bullet_speed *= 1.2
          # Increase bullet speed by 10%
            
    def _update_aliens(self):
        """Update position of all aliens in the fleet"""
        self._check_fleet_edges()
        for alien in self.aliens.sprites():
            alien.update()

    def _create_fleet(self):
        """Create fleet of aliens"""
        alien = Alien(self, self.explosion_images)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - 3 * alien_width
        available_space_y = self.settings.screen_height - 2 * alien_height
        num_aliens_x = available_space_x // (2 * alien_width)
        num_aliens_y = available_space_y // (2 * alien_height)

        for row_number in range(num_aliens_y):
            for alien_number in range(num_aliens_x):
                x_position = alien_width + 1.75 * alien_width * alien_number
                y_position = alien_height + 1.75 * alien_height * row_number
                self._create_alien(x_position, y_position)

        # Reset ship to center
        self.ship.center_ship()

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the specified position"""
        alien = Alien(self, self.explosion_images)
        alien_width, alien_height = alien.rect.size
        alien.x = x_position
        alien.rect.x = alien.x
        alien.rect.y = y_position
        self.aliens.add(alien)

    def _check_fleet_edges_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                return True
        return False

    def _change_fleet_direction(self):
        """Drop the entire fleet and change fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _check_fleet_edges(self):
        """Check if any alien in the fleet has reached the edge of the screen"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _ship_hit(self):
        """Respond to ship being hit by an alien"""
        if self.lives > 0:
            self.lives -= 1
            print("Lives reduced to:", self.lives)
            if self.lives == 0:
                print("Game over due to lives reaching zero!")
                self._end_game()
            else:
                print("Resetting ship...")
                self.ship.center_ship()
                self.aliens.empty()
                self.bullets.empty()
                self._create_fleet()
                self._display_lives()  # Update the display after decrementing lives
            
    def _check_ship_alien_collision(self):
        if not self.collision_detected:
            if pygame.sprite.spritecollideany(self.ship, self.aliens):
                self.collision_detected = True  # Set collision flag to True
                self._ship_hit()
                pygame.time.delay(1000) # 1 second cooldown to allow a game pause

    def _display_score(self):
        """Display score on the screen"""
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        # Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        self._display_score()
        self._display_lives()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
    
        pygame.display.flip()

    def _display_lives(self):
        """Display the number of lives remaining"""
        lives_str = "Lives: " + str(self.lives)
        font = pygame.font.Font(None, 36)
        lives_text = font.render(lives_str, True, (255, 255, 255))
        self.screen.blit(lives_text, (10, 90))

    def _end_game(self):
        """End Game"""
        # Check if the player achieved a new high score
        if self.score > self.high_score:
            self.high_score = self.score
            self.leaderboard.display_leaderboard(self.screen, self.settings, self.score)
            

        # Fill the screen with a message indicating the game is over   
        self.screen.fill((30, 30, 30))  # Fill screen with black
        font = pygame.font.Font(None, 60)
        text = font.render("MISSION FAILED", True, (255, 102, 0))
        text_rect = text.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(2)

        high_scores_file = os.path.join(os.path.dirname(__file__), "high_scores.txt")
        # Display leaderboard
        self.leaderboard.display_leaderboard(self.screen, self.settings, self.score)

        # Delay  before exiting game
        time.sleep(5)
        sys.exit()

        # Calculate border position and size based on text dimensions
        border_width = text_rect.width + 40
        border_height = text_rect.height + 40
        border_x = (self.settings.screen_width - border_width) // 2
        border_y = (self.settings.screen_height - border_height) // 2

        # Draw vintage-style border
        pygame.draw.rect(self.screen, (255, 102, 0), (border_x, border_y, border_width, border_height), 10)

        # Blit text onto the screen
        self.screen.blit(text, text_rect)

        pygame.display.flip()
        time.sleep(3)
        sys.exit()
 
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game() 
