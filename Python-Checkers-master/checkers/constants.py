import pygame

WIDTH, HEIGHT = 800, 800
SCOREBOARD_HEIGHT = 80
TOTAL_HEIGHT = HEIGHT + SCOREBOARD_HEIGHT
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

# rgb
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREY = (128,128,128)

# Board colors (green / cream style)
LIGHT_SQUARE = (238, 238, 210)
DARK_SQUARE = (118, 150, 86)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))
