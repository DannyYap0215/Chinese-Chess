import pygame as pyg
import os
import time

# Ensure script runs from the correct folder
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Initialize pygame
pyg.init()

# Load images
board_path = "images/map new cords.png"
title_path = "images/zgxq.png"

# Load board and title images
board_image = pyg.image.load(board_path)
title_image = pyg.image.load(title_path)

# Get board dimensions
BOARD_WIDTH, BOARD_HEIGHT = board_image.get_width(), board_image.get_height()

# Set screen size (extra space on top for the title)
PADDING_TOP = 150  # Space for title
WIDTH, HEIGHT = BOARD_WIDTH, BOARD_HEIGHT + PADDING_TOP
screen = pyg.display.set_mode((WIDTH, HEIGHT))
pyg.display.set_caption("Chinese Chess (Xiangqi)")

# Resize title if needed
title_width = 300
title_height = 120
title_image = pyg.transform.scale(title_image, (title_width, title_height))

# Load title background image
title_bg_path = "images/titleBG.png"  # Make sure the image is saved in the 'images' folder
title_bg = pyg.image.load(title_bg_path)
title_bg = pyg.transform.scale(title_bg, (WIDTH, PADDING_TOP))

# Load sound effects
select_sound_path = "sounds/move-check.wav"
move_check_sound_path = "sounds/move-self.wav"

# Check if sound files exist before loading
select_sound = pyg.mixer.Sound(select_sound_path) if os.path.exists(select_sound_path) else None
move_check_sound = pyg.mixer.Sound(move_check_sound_path) if os.path.exists(move_check_sound_path) else None

# Timer settings
font = pyg.font.Font(None, 80)
start_time = time.time()

# Chessboard grid settings
ROWS, COLS = 10, 9  # Xiangqi has a 9x10 board
CELL_SIZE = BOARD_WIDTH // COLS
PIECE_RADIUS = 38  # Piece size

# Standard Xiangqi piece positions with correct labels
red_pieces = {
    (0, 0): "RR", (8, 0): "RR", (1, 0): "RH", (7, 0): "RH", (2, 0): "RE", (6, 0): "RE",
    (3, 0): "RA", (5, 0): "RA", (4, 0): "RG", (1, 2): "RC", (7, 2): "RC",
    (0, 3): "RS", (2, 3): "RS", (4, 3): "RS", (6, 3): "RS", (8, 3): "RS"
}

black_pieces = {
    (0, 9): "BR", (8, 9): "BR", (1, 9): "BH", (7, 9): "BH", (2, 9): "BE", (6, 9): "BE",
    (3, 9): "BA", (5, 9): "BA", (4, 9): "BG", (1, 7): "BC", (7, 7): "BC",
    (0, 6): "BS", (2, 6): "BS", (4, 6): "BS", (6, 6): "BS", (8, 6): "BS"
}

# Track the selected piece
selected_piece = None  # (col, row) tuple or None

# Function to draw pieces
def draw_pieces(surface):
    font = pyg.font.Font(None, 40)
    
    for (col, row), piece in {**red_pieces, **black_pieces}.items():
        px = col * CELL_SIZE + CELL_SIZE // 2
        py = row * CELL_SIZE + CELL_SIZE // 2 + PADDING_TOP
        
        # Determine color
        color = (0, 0, 0) if piece[0] == "B" else (255, 0, 0)  # Black or red

        # Highlight selected piece
        if selected_piece == (col, row):
            color = (255, 255, 255)  # White for selected piece

        pyg.draw.circle(surface, color, (px, py), PIECE_RADIUS)
        label = font.render(piece, True, (255, 255, 255))
        surface.blit(label, (px - 18, py - 12))

def player_turn(surface):
    font = pyg.font.Font(None, 55)
    player_now = "Black's Turn"
    player_now_text = font.render(player_now, True, (0, 0, 0))
    surface.blit(player_now_text, (535, 55))

class Game:
    """Handles the game state."""
    def draw(self, surface):
        surface.fill((50, 21, 21))  # Background color
        surface.blit(title_bg, (0, 0))  # Draw title background
        surface.blit(title_image, ((WIDTH - title_width) // 2, 10))  # Draw title text
        surface.blit(board_image, (0, PADDING_TOP))  # Draw board

        # Draw timer
        elapsed_time = int(time.time() - start_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        timer_text = f"{minutes:02}:{seconds:02}"
        timer_surface = font.render(timer_text, True, (0, 0, 0))
        surface.blit(timer_surface, (20, 45))

        # Draw pieces
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
        elif event.type == pyg.MOUSEBUTTONDOWN:
            mx, my = pyg.mouse.get_pos()
            col = mx // CELL_SIZE
            row = (my - PADDING_TOP) // CELL_SIZE

            # Check if clicked on a piece
            if (col, row) in red_pieces or (col, row) in black_pieces:
                if selected_piece == (col, row):  
                    # Deselect if clicking the same piece again
                    selected_piece = None

                    # Play move-check sound when deselecting
                    if move_check_sound:
                        move_check_sound.play()
                else:
                    # Select new piece
                    selected_piece = (col, row)

                    # Play select sound when selecting a piece
                    if select_sound:
                        select_sound.play()

    pyg.display.flip()
    clock.tick(60)

pyg.quit()
