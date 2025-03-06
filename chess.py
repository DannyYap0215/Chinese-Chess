import pygame as pyg
import os
import time

# Ensure script runs from correct folder
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Initialize pygame
pyg.init()

# Load images
board_path = "images\\map new cords.png"
title_path = "images\\zgxq.png"

# Load board and title images
board_image = pyg.image.load(board_path)
title_image = pyg.image.load(title_path)

# Get board dimensions
BOARD_WIDTH, BOARD_HEIGHT = board_image.get_width(), board_image.get_height()

# Resize title if needed
title_width = 300
title_height = 120
title_image = pyg.transform.scale(title_image, (title_width, title_height))

# Set screen size (extra space on top for the title)
PADDING_TOP = 150  # Space for title
WIDTH, HEIGHT = BOARD_WIDTH, BOARD_HEIGHT + PADDING_TOP
screen = pyg.display.set_mode((WIDTH, HEIGHT))
pyg.display.set_caption("Chinese Chess (Xiangqi)")

# Timer settings
font = pyg.font.Font(None, 80)
start_time = time.time()

# Chessboard grid settings
ROWS, COLS = 10, 9  # Xiangqi has a 9x10 board
CELL_SIZE = BOARD_WIDTH // COLS
PIECE_RADIUS = 38  # Piece size

# Standard Xiangqi piece positions
red_positions =     [(0, 0), (8, 0),    # Chariots
                    (4, 0),          # General
                    (3, 0), (5, 0),  # Advisors
                    (2, 0), (6, 0),  # Elephants
                    (1, 0), (7, 0),  # Horses
                    (1, 2), (7, 2),  # Canons
                    (0, 3), (2, 3), (4, 3), (6, 3), (8, 3)   # Soldiers
                    ] 

black_positions =   [(0, 9), (8, 9),  # Chariots
                    (4, 9),          # General
                    (3, 9), (5, 9),  # Advisors
                    (2, 9), (6, 9),  # Elephants
                    (1, 9), (7, 9),  # Horses
                    (1, 7), (7, 7),  # Canons
                    (0, 6), (2, 6), (4, 6), (6, 6), (8, 6)   # Soldiers
                    ] 

def player_turn(surface):
    font = pyg.font.Font(None, 55)
    player_now = "Black's Turn"
    player_now_text =  font.render(player_now, True, (0, 0, 0))
    surface.blit(player_now_text, (535, 55))

def draw_pieces(surface):
    """Draws only the piece positions."""
    for col, row in black_positions:
        px = col * CELL_SIZE + CELL_SIZE // 2
        py = row * CELL_SIZE + CELL_SIZE // 2 + PADDING_TOP
        pyg.draw.circle(surface, (0, 0, 0), (px, py), PIECE_RADIUS)  # Black pieces
    
    for col, row in red_positions:
        px = col * CELL_SIZE + CELL_SIZE // 2
        py = row * CELL_SIZE + CELL_SIZE // 2 + PADDING_TOP
        pyg.draw.circle(surface, (255, 0, 0), (px, py), PIECE_RADIUS)  # Red pieces

class Game:
    """Handles the game state."""
    def draw(self, surface):
        surface.fill((255, 255, 255))  # White background
        surface.blit(title_image, ((WIDTH - title_width) // 2, 10))  # Title centered above board
        surface.blit(board_image, (0, PADDING_TOP))  # Board below title
        
        # Draw timer
        elapsed_time = int(time.time() - start_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        timer_text = f"{minutes:02}:{seconds:02}"
        timer_surface = font.render(timer_text, True, (0, 0, 0))  # Black text
        surface.blit(timer_surface, (20, 45))  # Position on the left
        
        # Draw only chess piece positions
        draw_pieces(surface)
        player_turn(surface)

# Main game loop
game = Game()
clock = pyg.time.Clock()
running = True

while running:
    screen.fill((255, 255, 255))  # White background
    game.draw(screen)

    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            running = False

    pyg.display.flip()
    clock.tick(60)

pyg.quit()
