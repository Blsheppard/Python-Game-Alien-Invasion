import pygame
import sys
import os

class Leaderboard:
    def __init__(self, high_scores_file):
        self.high_scores_file = os.path.join(os.path.dirname(__file__), high_scores_file)
        self.entering_initials = False
        self.player_initials = ""

    def load_high_scores(self):
        try:
            with open(self.high_scores_file, 'r') as file:
                lines = file.readlines()
                high_scores = [(line.split(':')[0], int(line.split(':')[1])) for line in lines]
                return sorted(high_scores, key=lambda x: x[1], reverse=True)
        except FileNotFoundError:
            with open(self.high_scores_file, 'w') as file:
                default_scores = [('AAA', 0)] * 10
                for initials, score in default_scores:
                    file.write(f"{initials}:{score}\n")
                return default_scores
            
    def update_high_scores(self, initials, score):
        high_scores = self.load_high_scores()
        high_scores.append((initials, score))
        high_scores.sort(key=lambda x: x[1], reverse=True)
        high_scores = high_scores[:10]  # Keep only top 10 scores
        with open(self.high_scores_file, 'w') as file:
            for initials, score in high_scores:
                file.write(f"{initials}:{score}\n")

    def display_leaderboard(self, screen, settings, final_score):
        """Display leaderboard and allow initials entry"""
        self.entering_initials = True
        self.player_initials = ""
        self.final_score = final_score  # Store the final score
    
        while self.entering_initials:
            screen.fill((30, 30, 30))

            title_font = pygame.font.Font(None, 50)
            score_font = pygame.font.Font(None, 30)

            title_text = title_font.render("HIGH SCORES", True, (255, 255, 0))
            title_rect = title_text.get_rect(center=(settings.screen_width // 2, 50))
            screen.blit(title_text, title_rect)

            high_scores = self.load_high_scores()

            x_position = settings.screen_width // 4
            y_position = 150
            for i, (initials, score) in enumerate(high_scores):
                score_text = score_font.render(f"{initials}: {score}", True, (255, 255, 255))
                score_rect = score_text.get_rect(center=(x_position, y_position + i * 40))
                screen.blit(score_text, score_rect)

            initials_prompt = score_font.render("Enter Your Initials:", True, (255, 255, 255))
            initials_prompt_rect = initials_prompt.get_rect(center=(settings.screen_width // 2, 400))

            player_initials_text = score_font.render(self.player_initials, True, (255, 255, 255))
            player_initials_rect = player_initials_text.get_rect(center=(settings.screen_width // 2, 450))

            screen.blit(initials_prompt, initials_prompt_rect)
            screen.blit(player_initials_text, player_initials_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.update_high_scores(self.player_initials, self.final_score)  # Use final_score here
                        self.entering_initials = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_initials = self.player_initials[:-1]
                    elif len(self.player_initials) < 3 and event.unicode.isalpha():
                        self.player_initials += event.unicode