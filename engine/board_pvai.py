
import os
import pygame
import pygame_gui

pygame.init()

WIDTH, HEIGHT = 1200, 800
FPS = 60

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cờ Tướng – PVAI Only")
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

# PVAI panel only
pvai_panel = pygame_gui.elements.UIPanel(
    relative_rect=pygame.Rect(0, 0, 400, 800),
    manager=ui_manager,
    container=control_panel,
    starting_height=2
)

# Buttons
pvai_buttons = ['New Game', 'Undo', 'Hint', 'Save', 'Load', 'Swap Sides']
for i, label in enumerate(pvai_buttons):
    pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(10 + (i % 2) * 190, 10 + (i // 2) * 44, 180, 34),
        text=label,
        manager=ui_manager,
        container=pvai_panel
    )

# AI selection
pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(10, 150, 80, 24),
    text="AI plays:",
    manager=ui_manager,
    container=pvai_panel
)
pvai_side_dropdown = pygame_gui.elements.UIDropDownMenu(
    options_list=["Black", "Red"],
    starting_option="Black",
    relative_rect=pygame.Rect(95, 148, 120, 28),
    manager=ui_manager,
    container=pvai_panel
)
pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(230, 150, 60, 24),
    text="Level:",
    manager=ui_manager,
    container=pvai_panel
)
pvai_level_dropdown = pygame_gui.elements.UIDropDownMenu(
    options_list=["Easy", "Medium", "Hard"],
    starting_option="Medium",
    relative_rect=pygame.Rect(290, 148, 100, 28),
    manager=ui_manager,
    container=pvai_panel
)
pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(10, 182, 180, 30),
    text="Start AI",
    manager=ui_manager,
    container=pvai_panel
)
pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(210, 182, 180, 30),
    text="Stop AI",
    manager=ui_manager,
    container=pvai_panel
)

# Move list and status
pvai_moves = pygame_gui.elements.UITextBox(
    html_text="<b>Move List</b><br/>",
    relative_rect=pygame.Rect(10, 220, 380, 420),
    manager=ui_manager,
    container=pvai_panel
)
pvai_status = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(10, 650, 380, 26),
    text="Tới lượt Đỏ (AI: Đen)",
    manager=ui_manager,
    container=pvai_panel
)

# Load pieces
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
