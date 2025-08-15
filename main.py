import pygame
import sys
import webbrowser
from pygame.locals import *

# Khởi tạo Pygame
pygame.init()

# Kích thước và FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 550, 800
FPS = 60
fpsClock = pygame.time.Clock()

# Tạo cửa sổ
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Game Cờ Tướng')

# === LOAD HÌNH ẢNH ===

# Background
background_img = pygame.image.load('assets/UI/background.png')
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Nút góc trên
btn_setting_img = pygame.image.load('assets/UI/btn_setting.png')
btn_setting_img = pygame.transform.scale(btn_setting_img, (80, 80))

btn_exit_img = pygame.image.load('assets/UI/btn_exit.png')
btn_exit_img = pygame.transform.scale(btn_exit_img, (80, 80))

# Logo
logo_img = pygame.image.load('assets/UI/logo.png')
logo_img = pygame.transform.scale(logo_img, (200, 200))
logo_x = (SCREEN_WIDTH - 200) // 2
logo_y = 130

# Nút chơi game
btn_play_ai_img = pygame.image.load('assets/UI/btn_pvai.png')
btn_play_ai_img = pygame.transform.scale(btn_play_ai_img, (420, 140))

btn_play_pvp_img = pygame.image.load('assets/UI/btn_pvp.png')
btn_play_pvp_img = pygame.transform.scale(btn_play_pvp_img, (420, 140))

# Căn giữa nút 420px theo chiều ngang
btn_game_width, btn_game_height = 420, 150
btn_ai_x = (SCREEN_WIDTH - btn_game_width) // 2

# Vị trí theo chiều dọc
btn_ai_y = logo_y + 200 + 30  # dưới logo 30px
btn_pvp_y = btn_ai_y + btn_game_height + 0  # cách nhau 40px

# === ICON DƯỚI CÙNG ===

icon_size = (80, 80)
icon_y = SCREEN_HEIGHT - icon_size[1] - 30  # cách bottom 30px

# Load và scale icon
icon_facebook_img = pygame.image.load('assets/UI/icon_facebook.png')
icon_facebook_img = pygame.transform.scale(icon_facebook_img, icon_size)

icon_rules_img = pygame.image.load('assets/UI/icon_rules.png')
icon_rules_img = pygame.transform.scale(icon_rules_img, icon_size)

icon_github_img = pygame.image.load('assets/UI/icon_github.png')
icon_github_img = pygame.transform.scale(icon_github_img, icon_size)

# Vị trí icon dưới cùng (căn với setting, exit, center)
facebook_x = 60
github_x = 410
rules_x = (SCREEN_WIDTH - icon_size[0]) // 2


# === LỚP BUTTON DẠNG ẢNH ===
class ImageButton:
    def __init__(self, image, x, y, callback=None):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.callback = callback

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


# === CÁC HÀM SỰ KIỆN ===
def on_setting_click():
    print("→ CÀI ĐẶT")

def on_exit_click():
    print("→ THOÁT GAME")
    pygame.quit()
    sys.exit()

def on_ai_click():
    print("→ CHƠI VỚI MÁY")

def on_pvp_click():
    print("→ HAI NGƯỜI CHƠI")

def on_facebook_click():
    print("→ FACEBOOK")
    webbrowser.open("https://www.facebook.com")

def on_rules_click():
    print("→ LUẬT CHƠI")
    webbrowser.open("https://banco.vn/Luat-choi-co-tuong_c_975.html")

def on_github_click():
    print("→ GITHUB")
    webbrowser.open("https://github.com/khongphaihoang/co_tuong_AI")

# === TẠO BUTTON ===
setting_button = ImageButton(btn_setting_img, 60, 30, on_setting_click)
exit_button = ImageButton(btn_exit_img, 410, 30, on_exit_click)

ai_button = ImageButton(btn_play_ai_img, btn_ai_x, btn_ai_y, on_ai_click)
pvp_button = ImageButton(btn_play_pvp_img, btn_ai_x, btn_pvp_y, on_pvp_click)

facebook_button = ImageButton(icon_facebook_img, facebook_x, icon_y, on_facebook_click)
rules_button = ImageButton(icon_rules_img, rules_x, icon_y, on_rules_click)
github_button = ImageButton(icon_github_img, github_x, icon_y, on_github_click)


# === VÒNG LẶP CHÍNH ===
while True:
    # Vẽ background
    DISPLAYSURF.blit(background_img, (0, 0))

    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for button in [
                setting_button, exit_button,
                ai_button, pvp_button,
                facebook_button, rules_button, github_button
            ]:
                if button.is_clicked(mouse_pos) and button.callback:
                    button.callback()

    # Vẽ UI
    setting_button.draw(DISPLAYSURF)
    exit_button.draw(DISPLAYSURF)
    DISPLAYSURF.blit(logo_img, (logo_x, logo_y))
    ai_button.draw(DISPLAYSURF)
    pvp_button.draw(DISPLAYSURF)
    facebook_button.draw(DISPLAYSURF)
    rules_button.draw(DISPLAYSURF)
    github_button.draw(DISPLAYSURF)

    # Cập nhật màn hình
    pygame.display.update()
    fpsClock.tick(FPS)
