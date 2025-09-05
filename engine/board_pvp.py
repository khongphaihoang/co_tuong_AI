import os
from typing import Dict, Tuple, List, Optional

import pygame
import pygame_gui

pygame.init()

# ===================== UI & BÀN CỜ =====================
WIDTH, HEIGHT = 1200, 800
FPS = 60

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cờ Tướng – PVP")
clock = pygame.time.Clock()

base_path = os.path.dirname(os.path.abspath(__file__))
board_img_path = os.path.join(base_path, '..', 'assets', 'UI', 'board.png')
board_img = pygame.image.load(board_img_path).convert_alpha()
board_img = pygame.transform.scale(board_img, (800, 800))

BOARD_X, BOARD_Y = 0, 0
INNER_MARGIN_X, INNER_MARGIN_Y = 40, 40  # lề trong của bàn vẽ
CELL_W = (800 - 2 * INNER_MARGIN_X) / 8
CELL_H = (800 - 2 * INNER_MARGIN_Y) / 9

def grid_to_px(col, row):
    x = BOARD_X + INNER_MARGIN_X + col * CELL_W
    y = BOARD_Y + INNER_MARGIN_Y + row * CELL_H
    return int(x), int(y)

def px_to_grid(px, py) -> Optional[Tuple[int, int]]:
    if not (BOARD_X <= px <= BOARD_X + 800 and BOARD_Y <= py <= BOARD_Y + 800):
        return None
    # đưa về gần tâm ô
    col_float = (px - BOARD_X - INNER_MARGIN_X) / CELL_W
    row_float = (py - BOARD_Y - INNER_MARGIN_Y) / CELL_H
    col = round(col_float)
    row = round(row_float)
    if 0 <= col <= 8 and 0 <= row <= 9:
        return col, row
    return None

ui_manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Panel điều khiển bên phải
control_panel = pygame_gui.elements.UIPanel(
    relative_rect=pygame.Rect(800, 0, 400, 800),
    starting_height=1,
    manager=ui_manager
)

pvp_panel = pygame_gui.elements.UIPanel(
    relative_rect=pygame.Rect(0, 0, 400, 800),
    manager=ui_manager,
    container=control_panel,
    starting_height=2
)

# Nút cơ bản (tối giản để tập trung 2 yêu cầu)
btn_new = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(10, 10, 120, 34),
    text="New Game",
    manager=ui_manager, container=pvp_panel
)
btn_undo = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(140, 10, 120, 34),
    text="Undo",
    manager=ui_manager, container=pvp_panel
)
btn_redo = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(270, 10, 120, 34),
    text="Redo",
    manager=ui_manager, container=pvp_panel
)

pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(10, 56, 380, 22),
    text="Danh sách nước đi",
    manager=ui_manager, container=pvp_panel
)
moves_box = pygame_gui.elements.UITextBox(
    html_text="",
    relative_rect=pygame.Rect(10, 80, 380, 500),
    manager=ui_manager, container=pvp_panel
)

status_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(10, 590, 380, 26),
    text="",
    manager=ui_manager, container=pvp_panel
)

# ===================== KIỂU DỮ LIỆU & LUẬT =====================
Pos = Tuple[int, int]   # (col,row)
Piece = Dict[str, str]  # {'color': 'red'|'black', 'name': '...'}
Board = Dict[Pos, Piece]

def in_bounds(c: int, r: int) -> bool:
    return 0 <= c < 9 and 0 <= r < 10

def in_palace(color: str, c: int, r: int) -> bool:
    # Cột 3..5. Đen ở hàng 0..2, Đỏ ở hàng 7..9
    if c < 3 or c > 5:
        return False
    return (0 <= r <= 2) if color == 'black' else (7 <= r <= 9)

def empty_between_files(board: Board, c: int, r1: int, r2: int) -> bool:
    a, b = sorted((r1, r2))
    for rr in range(a + 1, b):
        if (c, rr) in board:
            return False
    return True

def find_general(board: Board, color: str) -> Optional[Pos]:
    for (c, r), p in board.items():
        if p['name'] == 'general' and p['color'] == color:
            return (c, r)
    return None

def generals_face(board: Board) -> bool:
    """Hai tướng đối mặt (cùng cột và không có quân cản)."""
    rg = find_general(board, 'red')
    bg = find_general(board, 'black')
    if not rg or not bg:
        return False
    if rg[0] != bg[0]:
        return False
    return empty_between_files(board, rg[0], rg[1], bg[1])

def ray(board: Board, c: int, r: int, dc: int, dr: int) -> List[Pos]:
    out = []
    nc, nr = c + dc, r + dr
    while in_bounds(nc, nr) and (nc, nr) not in board:
        out.append((nc, nr))
        nc += dc; nr += dr
    return out

def cannon_captures(board: Board, c: int, r: int, dc: int, dr: int) -> List[Pos]:
    # pháo phải có "màn" để ăn
    nc, nr = c + dc, r + dr
    while in_bounds(nc, nr) and (nc, nr) not in board:
        nc += dc; nr += dr
    if not in_bounds(nc, nr):
        return []
    # gặp màn rồi, ô kế tiếp theo hướng nếu có quân đối phương thì ăn
    nc += dc; nr += dr
    while in_bounds(nc, nr):
        if (nc, nr) in board:
            return [(nc, nr)]
        nc += dc; nr += dr
    return []

def pseudo_moves_for_piece(board: Board, pos: Pos) -> List[Pos]:
    """Nước đi thô theo quân (chưa lọc tự chiếu/đối mặt)."""
    c, r = pos
    p = board[pos]; color, name = p['color'], p['name']
    moves: List[Pos] = []

    if name == 'general':
        for dc, dr in [(1,0),(-1,0),(0,1),(0,-1)]:
            nc, nr = c+dc, r+dr
            if in_bounds(nc,nr) and in_palace(color, nc, nr):
                if (nc,nr) not in board or board[(nc,nr)]['color'] != color:
                    moves.append((nc,nr))
        # tướng có thể chiếu thẳng nếu không có quân cản
        other = 'black' if color == 'red' else 'red'
        og = find_general(board, other)
        if og and og[0] == c and empty_between_files(board, c, r, og[1]):
            moves.append(og)
        return moves

    if name == 'advisor':
        for dc, dr in [(1,1),(1,-1),(-1,1),(-1,-1)]:
            nc, nr = c+dc, r+dr
            if in_bounds(nc,nr) and in_palace(color, nc, nr):
                if (nc,nr) not in board or board[(nc,nr)]['color'] != color:
                    moves.append((nc,nr))
        return moves

    if name == 'elephant':
        for dc, dr in [(2,2),(2,-2),(-2,2),(-2,-2)]:
            nc, nr = c+dc, r+dr
            eye = (c+dc//2, r+dr//2)
            if not in_bounds(nc,nr): continue
            # tượng không qua sông
            if (color == 'black' and nr > 4) or (color == 'red' and nr < 5):
                continue
            # chặn mắt tượng
            if eye in board:
                continue
            if (nc,nr) not in board or board[(nc,nr)]['color'] != color:
                moves.append((nc,nr))
        return moves

    if name == 'horse':
        legs = [((1,0), (2,1)), ((1,0), (2,-1)), ((-1,0), (-2,1)), ((-1,0), (-2,-1)),
                ((0,1), (1,2)), ((0,1), (-1,2)), ((0,-1), (1,-2)), ((0,-1), (-1,-2))]
        for (lb, la) in legs:
            block = (c+lb[0], r+lb[1])
            nc, nr = c+la[0], r+la[1]
            if not in_bounds(nc,nr): continue
            if block in board: continue  # chân ngựa bị chặn
            if (nc,nr) not in board or board[(nc,nr)]['color'] != color:
                moves.append((nc,nr))
        return moves

    if name == 'chariot':
        for dc, dr in [(1,0),(-1,0),(0,1),(0,-1)]:
            for nc, nr in ray(board, c, r, dc, dr):
                moves.append((nc,nr))
            # ô ăn đầu tiên theo hướng
            nc, nr = c+dc, r+dr
            while in_bounds(nc,nr):
                if (nc,nr) in board:
                    if board[(nc,nr)]['color'] != color:
                        moves.append((nc,nr))
                    break
                nc += dc; nr += dr
        return moves

    if name == 'cannon':
        for dc, dr in [(1,0),(-1,0),(0,1),(0,-1)]:
            moves.extend(ray(board, c, r, dc, dr))             # đi
            moves.extend(cannon_captures(board, c, r, dc, dr)) # ăn
        return moves

    if name == 'soldier':
        fwd = 1 if color == 'black' else -1
        # tiến
        nr = r + fwd
        if in_bounds(c, nr) and ((c, nr) not in board or board[(c,nr)]['color'] != color):
            moves.append((c, nr))
        # qua sông được đi ngang
        if (color == 'black' and r >= 5) or (color == 'red' and r <= 4):
            for dc in (-1, 1):
                nc = c + dc
                if in_bounds(nc, r) and ((nc, r) not in board or board[(nc,r)]['color'] != color):
                    moves.append((nc, r))
        return moves

    return moves

def simulate(board: Board, src: Pos, dst: Pos) -> Board:
    newb = {k: v.copy() for k, v in board.items()}
    piece = newb.pop(src)
    if dst in newb: newb.pop(dst)
    newb[dst] = piece
    return newb

def is_in_check(board: Board, color: str) -> bool:
    """Tướng 'color' đang bị chiếu?"""
    g = find_general(board, color)
    if not g:
        return False
    enemy = 'black' if color == 'red' else 'red'
    # ô tướng của mình có nằm trong tầm chiếu của quân địch?
    for pos, piece in board.items():
        if piece['color'] != enemy:
            continue
        if g in pseudo_moves_for_piece(board, pos):
            return True
    # “chống tướng” cũng coi như bị chiếu
    if generals_face(board):
        return True
    return False

def legal_moves_for(board: Board, src: Pos) -> List[Pos]:
    """Lọc nước hợp lệ: không để tự chiếu & không gây “đối mặt” sau khi đi."""
    if src not in board:
        return []
    color = board[src]['color']
    out: List[Pos] = []
    for dst in pseudo_moves_for_piece(board, src):
        nb = simulate(board, src, dst)
        # cấm “đối mặt”
        if generals_face(nb):
            continue
        # cấm tự chiếu
        if is_in_check(nb, color):
            continue
        out.append(dst)
    return out

# ===================== THẾ CỜ BAN ĐẦU & VẼ =====================
# Danh sách theo (color, name, col, row)
INITIAL_POSITIONS = [
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

def initial_board() -> Board:
    b: Board = {}
    for color, name, c, r in INITIAL_POSITIONS:
        b[(c, r)] = {'color': color, 'name': name}
    return b

pieces_cache: Dict[str, pygame.Surface] = {}

def _load_image_safe(path: str) -> Optional[pygame.Surface]:
    try:
        return pygame.image.load(path).convert_alpha()
    except Exception:
        return None

def load_piece(color: str, name: str) -> pygame.Surface:
    """
    Tải ảnh quân cờ. Tự động thử các biến thể tên file (lower/capitalize)
    để tránh lỗi tên như Soldier.png vs soldier.png.
    """
    key = f"{color}_{name}"
    if key in pieces_cache:
        return pieces_cache[key]

    candidates = [
        os.path.join(base_path, '..', 'assets', 'pieces', color, f"{name}.png"),
        os.path.join(base_path, '..', 'assets', 'pieces', color, f"{name.capitalize()}.png"),
        os.path.join(base_path, '..', 'assets', 'pieces', color, f"{name.upper()}.png"),
    ]
    img = None
    for p in candidates:
        img = _load_image_safe(p)
        if img is not None:
            break
    if img is None:
        # không tìm thấy => tạo ô trống tạm
        img = pygame.Surface((int(CELL_W*0.9), int(CELL_H*0.9)), pygame.SRCALPHA)
        pygame.draw.circle(img, (200, 50, 50, 255), (img.get_width()//2, img.get_height()//2), img.get_width()//2, 2)

    size = int(min(CELL_W, CELL_H) * 0.9)
    img = pygame.transform.smoothscale(img, (size, size))
    pieces_cache[key] = img
    return img

def draw_piece(surface, color, name, col, row):
    img = load_piece(color, name)
    cx, cy = grid_to_px(col, row)
    rect = img.get_rect(center=(cx, cy))
    surface.blit(img, rect)

# ===================== TRẠNG THÁI VÁN & LỊCH SỬ =====================
current_board: Board = initial_board()
turn: str = 'red'
selected: Optional[Pos] = None
valid_moves: List[Pos] = []

history: List[Board] = [initial_board()]
hist_index: int = 0
move_list: List[str] = []

def update_status():
    enemy = 'black' if turn == 'red' else 'red'
    status = f"Tới lượt {'Đỏ' if turn=='red' else 'Đen'}"
    # nếu bên sắp chơi đang bị chiếu thì báo luôn
    if is_in_check(current_board, turn):
        status += " — BÊN ĐANG ĐI ĐANG BỊ CHIẾU!"
    status_label.set_text(status)

def push_history(board: Board):
    global history, hist_index
    # cắt phần redo
    history = history[:hist_index+1]
    history.append({k: v.copy() for k, v in board.items()})
    hist_index += 1

def undo():
    global current_board, hist_index, turn, selected, valid_moves
    if hist_index > 0:
        hist_index -= 1
        current_board = {k: v.copy() for k, v in history[hist_index].items()}
        turn = 'black' if (hist_index % 2 == 1) else 'red'
        selected = None
        valid_moves = []
        if move_list:
            move_list.pop()
            moves_box.set_text("<br/>".join(move_list))
        update_status()

def redo():
    global current_board, hist_index, turn, selected, valid_moves
    if hist_index + 1 < len(history):
        hist_index += 1
        current_board = {k: v.copy() for k, v in history[hist_index].items()}
        turn = 'black' if (hist_index % 2 == 1) else 'red'
        selected = None
        valid_moves = []
        update_status()

def reset_game():
    global current_board, turn, selected, valid_moves, history, hist_index, move_list
    current_board = initial_board()
    turn = 'red'
    selected = None
    valid_moves = []
    history = [initial_board()]
    hist_index = 0
    move_list = []
    moves_box.set_text("")
    update_status()

def algebra(pos: Pos) -> str:
    # cột A..I, hàng 10..1 (thói quen phổ biến); bạn có thể đổi nếu muốn
    col, row = pos
    files = "ABCDEFGHI"
    ranks = "10987654321"  # map 0..9 -> "10..1"
    return f"{files[col]}{ranks[row]}"

def append_move_to_list(piece: Piece, src: Pos, dst: Pos, checked: bool):
    eaten = (dst in history[-1] and history[-1][dst]['color'] != piece['color'])
    name = piece['name']
    san = f"{'Đ' if piece['color']=='red' else 'Đen'}:{name} {algebra(src)}→{algebra(dst)}"
    if eaten: san += "x"
    if checked: san += "+"
    move_list.append(san)
    moves_box.set_text("<br/>".join(move_list))

# ===================== CLICK & CHƠI =====================
def handle_click(col: int, row: int):
    global selected, valid_moves, current_board, turn

    pos = (col, row)
    piece = current_board.get(pos)

    # Nếu đang chọn quân mới
    if selected is None:
        if piece is None:  # click vào ô trống
            return
        if piece['color'] != turn:  # không phải quân của mình
            return
        selected = pos
        valid_moves = legal_moves_for(current_board, selected)
        return

    # Đang có quân được chọn:
    if pos == selected:
        # bỏ chọn
        selected = None
        valid_moves = []
        return

    # Nếu click vào một ô hợp lệ -> thực hiện nước đi
    if pos in valid_moves:
        piece = current_board[selected]
        # áp dụng
        new_board = simulate(current_board, selected, pos)

        # chặn “đối mặt” (phòng hộ kép — dù legal_moves đã lọc)
        if generals_face(new_board):
            return

        # cập nhật ván
        current_board = new_board
        push_history(current_board)

        # phát hiện chiếu sau khi đi
        enemy = 'black' if turn == 'red' else 'red'
        checked = is_in_check(current_board, enemy)

        # cập nhật danh sách nước & trạng thái
        append_move_to_list(piece, selected, pos, checked)
        if checked:
            status_label.set_text(f"Chiếu tướng {'Đen' if enemy=='black' else 'Đỏ'}!")
        else:
            status_label.set_text(f"Tới lượt {'Đen' if enemy=='black' else 'Đỏ'}")

        # đổi lượt
        turn = enemy
        selected = None
        valid_moves = []
        return

    # Không phải nước hợp lệ -> nếu click vào quân cùng màu, chuyển chọn
    if piece is not None and piece['color'] == turn:
        selected = pos
        valid_moves = legal_moves_for(current_board, selected)
    else:
        # click linh tinh
        selected = None
        valid_moves = []

# ===================== VÒNG LẶP GAME =====================
def draw_selection(surface):
    if selected is None:
        return
    cx, cy = grid_to_px(selected[0], selected[1])
    pygame.draw.circle(surface, (30, 180, 250), (cx, cy), 20, 3)
    for mv in valid_moves:
        mx, my = grid_to_px(mv[0], mv[1])
        pygame.draw.circle(surface, (30, 180, 80), (mx, my), 10, 0)

reset_game()

running = True
while running:
    time_delta = clock.tick(FPS) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            g = px_to_grid(*event.pos)
            if g is not None:
                handle_click(*g)

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == btn_new:
                    reset_game()
                elif event.ui_element == btn_undo:
                    undo()
                elif event.ui_element == btn_redo:
                    redo()

        ui_manager.process_events(event)

    ui_manager.update(time_delta)

    # Vẽ bàn + quân
    window.blit(board_img, (BOARD_X, BOARD_Y))
    for (c, r), pc in current_board.items():
        draw_piece(window, pc['color'], pc['name'], c, r)

    # Highlight chọn/quỹ đạo
    draw_selection(window)

    # Vẽ UI
    ui_manager.draw_ui(window)
    pygame.display.update()

pygame.quit()
