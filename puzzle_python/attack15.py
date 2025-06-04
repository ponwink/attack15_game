import pygame
import sys
import random
import time

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PANEL_SIZE = 100
PANEL_GAP = 20
GAME_TIME = 60  # 60 seconds (1 minute)
PANEL_RESET_TIME = 15  # 15 seconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
GREEN = (144, 238, 144)
RED = (255, 99, 71)
YELLOW = (255, 255, 153)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Attack15")

# Font
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 36)
title_font = pygame.font.SysFont(None, 72)

class Panel:
    def __init__(self, x, y, value=None):
        self.x = x
        self.y = y
        self.value = value if value else random.randint(1, 9)
        self.selected = False
        self.reset_time = time.time() + PANEL_RESET_TIME
        self.rect = pygame.Rect(x, y, PANEL_SIZE, PANEL_SIZE)
    
    def draw(self, surface):
        # Draw panel background
        color = LIGHT_BLUE if self.selected else WHITE
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)  # Border
        
        # Draw number
        text = font.render(str(self.value), True, BLACK)
        text_rect = text.get_rect(center=(self.x + PANEL_SIZE // 2, self.y + PANEL_SIZE // 2))
        surface.blit(text, text_rect)
        
        # Draw timer bar
        remaining_time = self.reset_time - time.time()
        if remaining_time > 0:
            timer_width = (remaining_time / PANEL_RESET_TIME) * PANEL_SIZE
            timer_rect = pygame.Rect(self.x, self.y + PANEL_SIZE - 5, timer_width, 5)
            pygame.draw.rect(surface, GREEN, timer_rect)
    
    def reset(self):
        self.value = random.randint(1, 9)
        self.selected = False
        self.reset_time = time.time() + PANEL_RESET_TIME
        
    def is_expired(self):
        return time.time() > self.reset_time

class Button:
    def __init__(self, x, y, width, height, text, color=GRAY):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)  # Border
        
        text = font.render(self.text, True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)
        
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Game:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.score = 0
        self.panels = []
        self.selected_panels = []
        self.start_time = None
        self.game_over = False
        
        # Create panels in a 3x3 grid
        start_x = (SCREEN_WIDTH - (3 * PANEL_SIZE + 2 * PANEL_GAP)) // 2
        start_y = (SCREEN_HEIGHT - (3 * PANEL_SIZE + 2 * PANEL_GAP)) // 2
        
        for row in range(3):
            for col in range(3):
                x = start_x + col * (PANEL_SIZE + PANEL_GAP)
                y = start_y + row * (PANEL_SIZE + PANEL_GAP)
                self.panels.append(Panel(x, y))
    
    def start(self):
        self.start_time = time.time()
        self.game_over = False
    
    def get_remaining_time(self):
        if not self.start_time:
            return GAME_TIME
        elapsed = time.time() - self.start_time
        remaining = GAME_TIME - elapsed
        return max(0, remaining)
    
    def check_panel_expiration(self):
        for panel in self.panels:
            if panel.is_expired():
                self.score -= 10  # Penalty for expired panel
                panel.reset()
    
    def handle_click(self, pos):
        for i, panel in enumerate(self.panels):
            if panel.rect.collidepoint(pos):
                if panel.selected:
                    panel.selected = False
                    if panel in self.selected_panels:
                        self.selected_panels.remove(panel)
                else:
                    panel.selected = True
                    self.selected_panels.append(panel)
                break
        
        # Check if sum is 15
        if len(self.selected_panels) >= 2:
            total = sum(panel.value for panel in self.selected_panels)
            if total == 15:
                self.score += 15
                # Replace selected panels with new ones
                for panel in self.selected_panels:
                    panel.reset()
                self.selected_panels = []
    
    def draw(self, surface):
        # Draw panels
        for panel in self.panels:
            panel.draw(surface)
        
        # Draw score
        score_text = small_font.render(f"Score: {self.score}", True, BLACK)
        surface.blit(score_text, (20, 20))
        
        # Draw time remaining
        remaining = self.get_remaining_time()
        time_text = small_font.render(f"Time: {int(remaining)}s", True, BLACK)
        surface.blit(time_text, (SCREEN_WIDTH - 150, 20))
        
        # Draw sum of selected panels
        if self.selected_panels:
            total = sum(panel.value for panel in self.selected_panels)
            sum_text = small_font.render(f"Sum: {total}", True, BLACK)
            surface.blit(sum_text, (SCREEN_WIDTH // 2 - 50, 20))
        
        # Check if game is over
        if remaining <= 0:
            self.game_over = True
            
        if self.game_over:
            # Draw game over message
            game_over_text = title_font.render("Game Over!", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            surface.blit(game_over_text, text_rect)
            
            final_score_text = font.render(f"Final Score: {self.score}", True, BLACK)
            text_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            surface.blit(final_score_text, text_rect)

def main_menu():
    start_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 30, 200, 60, "Start")
    exit_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 60, "Exit")
    
    while True:
        screen.fill(WHITE)
        
        # Draw title
        title_text = title_font.render("Attack15", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(title_text, title_rect)
        
        # Draw buttons
        start_button.draw(screen)
        exit_button.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(event.pos):
                    game_loop()
                elif exit_button.is_clicked(event.pos):
                    pygame.quit()
                    sys.exit()
        
        pygame.display.flip()

def game_loop():
    game = Game()
    game.start()
    clock = pygame.time.Clock()
    
    back_button = Button(20, SCREEN_HEIGHT - 70, 120, 50, "Back", YELLOW)
    
    while True:
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game.game_over:
                    return  # Go back to main menu
                elif back_button.is_clicked(event.pos):
                    return  # Go back to main menu
                else:
                    game.handle_click(event.pos)
        
        if not game.game_over:
            game.check_panel_expiration()
        
        game.draw(screen)
        back_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main_menu()
