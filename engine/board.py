import pygame
import pygame_gui
import os
from pygame.locals import *

pygame.init()

# === Cấu hình ===
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60

# === Tạo cửa sổ ===
window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Cờ Tướng - UI Layout')

# === UI Manager ===
ui_manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# === Load ảnh bàn cờ với đường dẫn tuyệt đối ===
base_path = os.path.dirname(os.path.abspath(__file__))
board_img_path = os.path.join(base_path, '..', 'assets', 'UI', 'board.png')
board_img = pygame.image.load(board_img_path)
board_img = pygame.transform.scale(board_img, (800, 800))

# === Panel điều khiển (phải) ===
control_panel_rect = pygame.Rect(800, 0, 400, 800)
control_panel = pygame_gui.elements.UIPanel(relative_rect=control_panel_rect,
                                            starting_height=1,
                                            manager=ui_manager)

# === Các nút chức năng ===
button_width = 120
button_height = 40
button_padding = 10

button_labels = ['New Game', 'Undo', 'Redo', 'Save', 'Load', 'Hint', 'Swap Sides']
buttons = []

for i, label in enumerate(button_labels):
    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(20, 20 + i*(button_height + button_padding), button_width, button_height),
        text=label,
        container=control_panel,
        manager=ui_manager
    )
    buttons.append(button)

# === Chế độ chơi ===
mode_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(20, 350, 100, 30),
    text='Mode:',
    container=control_panel,
    manager=ui_manager
)

mode_dropdown = pygame_gui.elements.UIDropDownMenu(
    options_list=['PVP', 'PVE'],
    starting_option='PVP',
    relative_rect=pygame.Rect(120, 350, 120, 30),
    container=control_panel,
    manager=ui_manager
)

# === Độ khó ===
level_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(20, 390, 100, 30),
    text='Level:',
    container=control_panel,
    manager=ui_manager
)

level_dropdown = pygame_gui.elements.UIDropDownMenu(
    options_list=['Easy', 'Medium', 'Hard'],
    starting_option='Medium',
    relative_rect=pygame.Rect(120, 390, 120, 30),
    container=control_panel,
    manager=ui_manager
)

# === Move List (cuộn dọc) ===
move_list_textbox = pygame_gui.elements.UITextBox(
    html_text='Danh sách nước đi:<br>',
    relative_rect=pygame.Rect(20, 440, 360, 200),
    container=control_panel,
    manager=ui_manager
)

# === Status Bar ===
status_bar = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(0, 780, 1200, 20),
    text='Trạng thái: Đang chờ bắt đầu game...',
    manager=ui_manager
)

# === Main loop ===
running = True
while running:
    time_delta = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        ui_manager.process_events(event)

    ui_manager.update(time_delta)

    # Vẽ bàn cờ (bên trái)
    window_surface.blit(board_img, (0, 0))

    # Vẽ UI
    ui_manager.draw_ui(window_surface)

    pygame.display.update()

pygame.quit()
