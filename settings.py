class Settings:
    """Class to store all settings for Alien Invasion game"""

    def __init__(self):
        """Initailize game settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 130)
        self.initial_lives = 3

        # Alien settings
        self.alien_speed = 7
        self.fleet_drop_speed = 8
        # Fleet_direction of 1 represents right, -1 represents left
        self.fleet_direction = 1

        # Ship settings
        self.ship_speed = 10

        # Bullet settings
        self.bullet_speed = 5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 102, 0)
        self.bullets_allowed = 5
        
         # Alien settings
        self.aliens_per_row = 15
        self.alien_rows = 8