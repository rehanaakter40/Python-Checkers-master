import pygame
import random
from checkers.constants import WIDTH, HEIGHT, TOTAL_HEIGHT, SCOREBOARD_HEIGHT, SQUARE_SIZE, RED, WHITE, BLUE
from checkers.game import Game

pygame.init()
pygame.font.init()

FPS = 60

WIN = pygame.display.set_mode((WIDTH, TOTAL_HEIGHT))
pygame.display.set_caption('Checkers - Human (RED) vs Computer (WHITE)')

# Font for scoreboard and text
FONT_LARGE = pygame.font.Font(None, 60)
FONT_MEDIUM = pygame.font.Font(None, 40)
FONT_SMALL = pygame.font.Font(None, 30)

# Scoreboard
SCOREBOARD = {
    'human_wins': 0,
    'ai_wins': 0
}

# Celebration particles
particles = []

class Particle:
    def __init__(self, x, y, vx, vy, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.life = 60
        self.max_life = 60
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1  # gravity
        self.life -= 1
    
    def draw(self, win):
        if self.life > 0:
            alpha = int(255 * (self.life / self.max_life))
            size = max(2, int(10 * (self.life / self.max_life)))
            pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), size)

def create_celebration_particles(x, y, color, count=20):
    """Create celebration particles that burst from a point"""
    for _ in range(count):
        angle = random.random() * 2 * 3.14159
        speed = random.uniform(2, 6)
        vx = speed * random.uniform(-1, 1)
        vy = speed * random.uniform(-1, 1)
        particles.append(Particle(x, y, vx, vy, color))

def draw_scoreboard(win):
    """Draw the scoreboard at the top of the screen"""
    scoreboard_bg = pygame.Surface((WIDTH, SCOREBOARD_HEIGHT))
    scoreboard_bg.fill((50, 50, 50))
    win.blit(scoreboard_bg, (0, 0))
    
    human_text = FONT_SMALL.render(f"YOU (RED): {SCOREBOARD['human_wins']}", True, RED)
    ai_text = FONT_SMALL.render(f"AI (WHITE): {SCOREBOARD['ai_wins']}", True, WHITE)
    vs_text = FONT_SMALL.render("VS", True, BLUE)
    
    win.blit(human_text, (50, 20))
    win.blit(ai_text, (WIDTH - 300, 20))
    win.blit(vs_text, (WIDTH // 2 - 20, 25))

def draw_victory_screen(win, winner_color, winner_name):
    """Draw victory celebration screen with replay option"""
    # Semi-transparent overlay
    overlay = pygame.Surface((WIDTH, TOTAL_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    win.blit(overlay, (0, SCOREBOARD_HEIGHT))
    
    # Victory text - centered in the game board area, not including scoreboard
    victory_text = FONT_LARGE.render(f"{winner_name} WINS!", True, winner_color)
    victory_rect = victory_text.get_rect(center=(WIDTH // 2, SCOREBOARD_HEIGHT + HEIGHT // 2 - 100))
    win.blit(victory_text, victory_rect)
    
    # Replay instruction
    replay_text = FONT_SMALL.render("Press SPACE to play again or Q to quit", True, WHITE)
    replay_rect = replay_text.get_rect(center=(WIDTH // 2, SCOREBOARD_HEIGHT + HEIGHT // 2 + 50))
    win.blit(replay_text, replay_rect)
    
    # Draw celebration particles
    for particle in particles:
        particle.update()
        particle.draw(win)
    
    # Remove dead particles
    particles[:] = [p for p in particles if p.life > 0]

def get_row_col_from_mouse(pos):
    x, y = pos
    # Adjust for scoreboard offset
    y -= SCOREBOARD_HEIGHT
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    if row < 0 or row >= 8 or col < 0 or col >= 8:
        return None, None
    return row, col

def main():
    global particles
    
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    ai_thinking = False
    ai_start_time = 0
    game_over = False
    winner = None
    celebration_frames = 0
    
    while run:
        clock.tick(FPS)
        
        # Check for winner
        if game.winner() is not None and not game_over:
            game_over = True
            winner = game.winner()
            winner_name = "YOU (RED)" if winner == RED else "AI (WHITE)"
            
            # Update scoreboard
            if winner == RED:
                SCOREBOARD['human_wins'] += 1
            else:
                SCOREBOARD['ai_wins'] += 1
            
            # Create celebration particles from center
            for _ in range(50):
                create_celebration_particles(
                    WIDTH // 2, 
                    HEIGHT // 2, 
                    winner,
                    count=3
                )
            celebration_frames = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            # Replay option during game over screen
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_SPACE:
                    # Reset for new game
                    game = Game(WIN)
                    game_over = False
                    winner = None
                    particles = []
                    ai_thinking = False
                    celebration_frames = 0
                elif event.key == pygame.K_q:
                    run = False
            
            # Human controls RED pieces with the mouse (only if game not over)
            if event.type == pygame.MOUSEBUTTONDOWN and game.turn == RED and not game_over:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                if row is not None and col is not None:
                    game.select(row, col)

        # AI logic (only if game not over)
        if not game_over:
            # Start AI thinking delay when it becomes WHITE's turn
            if game.turn == WHITE and not ai_thinking and game.winner() is None:
                ai_thinking = True
                ai_start_time = pygame.time.get_ticks()

            # After 1 second of "thinking", let the computer play
            if ai_thinking and game.turn == WHITE and game.winner() is None:
                now = pygame.time.get_ticks()
                if now - ai_start_time >= 1000:
                    game.ai_move(WHITE)
                    ai_thinking = False

            # If turn changed back to RED (or game ended), stop thinking
            if game.turn != WHITE:
                ai_thinking = False

        # Draw game
        game.update()
        
        # Draw scoreboard
        draw_scoreboard(WIN)
        
        # Draw victory screen if game is over
        if game_over:
            celebration_frames += 1
            draw_victory_screen(WIN, winner, "YOU (RED)" if winner == RED else "AI (WHITE)")
        
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()