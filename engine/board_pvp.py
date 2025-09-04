
import os
import pygame
import pygame_gui

pygame.init()

WIDTH, HEIGHT = 1200, 800
FPS = 60

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cờ Tướng – PVP Only")
clock = pygame.time.Clock()

base_path = os.path.dirname(os.path.abspath(__file__))
board_img_path = os.path.join(base_path, '..', 'assets', 'UI', 'board.png')
board_img = pygame.image.load(board_img_path).convert_alpha()
board_img = pygame.transform.scale(board_img, (800, 800))

BOARD_X, BOARD_Y = 0, 0
INNER_MARGIN_X, INNER_MARGIN_Y = 40, 40
CELL_W = (800 - 2 * INNER_MARGIN_X) / 8
CELL_H = (800 - 2 * INNER_MARGIN_Y) / 9

def grid_to_px(col, row):
    x = BOARD_X + INNER_MARGIN_X + col * CELL_W
    y = BOARD_Y + INNER_MARGIN_Y + row * CELL_H
    return int(x), int(y)

ui_manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Control panel
control_panel = pygame_gui.elements.UIPanel(
    relative_rect=pygame.Rect(800, 0, 400, 800),
    starting_height=1,
    manager=ui_manager
)

# PVP panel only
pvp_panel = pygame_gui.elements.UIPanel(
    relative_rect=pygame.Rect(0, 0, 400, 800),
    manager=ui_manager,
    container=control_panel,
    starting_height=2
)

# Buttons
pvp_buttons = ['New Game', 'Undo', 'Redo', 'Save', 'Load', 'Swap Sides']
for i, label in enumerate(pvp_buttons):
    pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(10 + (i % 2) * 190, 10 + (i // 2) * 44, 180, 34),
        text=label,
        manager=ui_manager,
        container=pvp_panel
    )

# Player names
pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(10, 150, 70, 24),
    text="Red:",
    manager=ui_manager,
    container=pvp_panel
)
pvp_red_entry = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(80, 150, 300, 26),
    manager=ui_manager,
    container=pvp_panel
)
pvp_red_entry.set_text("Player Red")

pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(10, 182, 70, 24),
    text="Black:",
    manager=ui_manager,
    container=pvp_panel
)
pvp_black_entry = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(80, 182, 300, 26),
    manager=ui_manager,
    container=pvp_panel
)
pvp_black_entry.set_text("Player Black")

# Move list and status
pvp_moves = pygame_gui.elements.UITextBox(
    html_text="<b>Move List</b><br/>",
    relative_rect=pygame.Rect(10, 220, 380, 420),
    manager=ui_manager,
    container=pvp_panel
)
pvp_status = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(10, 650, 380, 26),
    text="Tới lượt Đỏ",
    manager=ui_manager,
    container=pvp_panel
)

# Load & scale piece images
pieces_cache = {}
def load_piece(color, name):
    key = f"{color}_{name}"
    if key in pieces_cache:
        return pieces_cache[key]
    piece_path = os.path.join(base_path, '..', 'assets', 'pieces', color, f"{name}.png")
    img = pygame.image.load(piece_path).convert_alpha()
    size = int(min(CELL_W, CELL_H) * 0.9)
    img = pygame.transform.smoothscale(img, (size, size))
    pieces_cache[key] = img
    return img

def draw_piece(surface, color, name, col, row):
    img = load_piece(color, name)
    cx, cy = grid_to_px(col, row)
    rect = img.get_rect(center=(cx, cy))
    surface.blit(img, rect)

# Initial positions
initial_positions = [
    # Black
    ('black', 'chariot', 0, 0), ('black', 'horse', 1, 0), ('black', 'elephant', 2, 0),
    ('black', 'advisor', 3, 0), ('black', 'general', 4, 0), ('black', 'advisor', 5, 0),
    ('black', 'elephant', 6, 0), ('black', 'horse', 7, 0), ('black', 'chariot', 8, 0),
    ('black', 'cannon', 1, 2), ('black', 'cannon', 7, 2),
    ('black', 'soldier', 0, 3), ('black', 'soldier', 2, 3), ('black', 'soldier', 4, 3),
    ('black', 'soldier', 6, 3), ('black', 'soldier', 8, 3),
    # Red
    ('red', 'chariot', 0, 9), ('red', 'horse', 1, 9), ('red', 'elephant', 2, 9),
    ('red', 'advisor', 3, 9), ('red', 'general', 4, 9), ('red', 'advisor', 5, 9),
    ('red', 'elephant', 6, 9), ('red', 'horse', 7, 9), ('red', 'chariot', 8, 9),
    ('red', 'cannon', 1, 7), ('red', 'cannon', 7, 7),
    ('red', 'soldier', 0, 6), ('red', 'soldier', 2, 6), ('red', 'soldier', 4, 6),
    ('red', 'soldier', 6, 6), ('red', 'soldier', 8, 6),
]

# Game loop
running = True
while running:
    time_delta = clock.tick(FPS) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        ui_manager.process_events(event)

    ui_manager.update(time_delta)

    window.blit(board_img, (BOARD_X, BOARD_Y))
    for color, name, c, r in initial_positions:
        draw_piece(window, color, name, c, r)

    ui_manager.draw_ui(window)
    pygame.display.update()

pygame.quit()
