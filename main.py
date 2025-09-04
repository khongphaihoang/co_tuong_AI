import pygame
import subprocess
import sys
import webbrowser
from pygame.locals import *

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 550, 800
FPS = 60
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Game Cờ Tướng')

# Load images
background_img = pygame.image.load('assets/UI/background.png')
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

btn_setting_img = pygame.image.load('assets/UI/btn_setting.png')
btn_setting_img = pygame.transform.scale(btn_setting_img, (80, 80))

btn_exit_img = pygame.image.load('assets/UI/btn_exit.png')
btn_exit_img = pygame.transform.scale(btn_exit_img, (80, 80))

logo_img = pygame.image.load('assets/UI/logo.png')
logo_img = pygame.transform.scale(logo_img, (200, 200))
logo_x = (SCREEN_WIDTH - 200) // 2
logo_y = 130
logo_height = 200

# Nút chơi game - scale chuẩn về cùng size
button_size = (420, 140)
btn_pvai_img = pygame.image.load('assets/UI/btn_pvai.png')
btn_pvai_img = pygame.transform.scale(btn_pvai_img, button_size)

btn_pvp_img = pygame.image.load('assets/UI/btn_pvp.png')
btn_pvp_img = pygame.transform.scale(btn_pvp_img, button_size)

btn_game_width, btn_game_height = button_size
btn_pvai_x = (SCREEN_WIDTH - btn_game_width) // 2
btn_pvai_y = logo_y + logo_height + 30
btn_pvp_y = btn_pvai_y + btn_game_height + 40

icon_size = (80, 80)
icon_y = SCREEN_HEIGHT - icon_size[1] - 30

icon_facebook_img = pygame.image.load('assets/UI/icon_facebook.png')
icon_facebook_img = pygame.transform.scale(icon_facebook_img, icon_size)

icon_rules_img = pygame.image.load('assets/UI/icon_rules.png')
icon_rules_img = pygame.transform.scale(icon_rules_img, icon_size)

icon_github_img = pygame.image.load('assets/UI/icon_github.png')
icon_github_img = pygame.transform.scale(icon_github_img, icon_size)

facebook_x = 60
github_x = 410
rules_x = (SCREEN_WIDTH - icon_size[0]) // 2

class ImageButton:
    def __init__(self, image, x, y, callback=None):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.callback = callback

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def on_setting_click():
    print("→ CÀI ĐẶT")

def on_exit_click():
    print("→ THOÁT GAME")
    pygame.quit()
    sys.exit()

def on_pvai_click():
    print("→ CHƠI VỚI MÁY")
    subprocess.Popen([sys.executable, "engine/board_pvai.py"])

def on_pvp_click():
    print("→ HAI NGƯỜI CHƠI")
    subprocess.Popen([sys.executable, "engine/board_pvp.py"])

def on_facebook_click():
    print("→ FACEBOOK")
    webbrowser.open("https://www.facebook.com")

def on_rules_click():
    print("→ LUẬT CHƠI")
    webbrowser.open("https://banco.vn/Luat-choi-co-tuong_c_975.html")

def on_github_click():
    print("→ GITHUB")
    webbrowser.open("https://github.com/khongphaihoang/co_tuong_AI")

setting_button = ImageButton(btn_setting_img, 60, 30, on_setting_click)
exit_button = ImageButton(btn_exit_img, 410, 30, on_exit_click)

pvai_button = ImageButton(btn_pvai_img, btn_pvai_x, btn_pvai_y, on_pvai_click)
pvp_button = ImageButton(btn_pvp_img, btn_pvai_x, btn_pvp_y, on_pvp_click)

facebook_button = ImageButton(icon_facebook_img, facebook_x, icon_y, on_facebook_click)
rules_button = ImageButton(icon_rules_img, rules_x, icon_y, on_rules_click)
github_button = ImageButton(icon_github_img, github_x, icon_y, on_github_click)

while True:
    DISPLAYSURF.blit(background_img, (0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for button in [
                setting_button, exit_button,
                pvai_button, pvp_button,
                facebook_button, rules_button, github_button
            ]:
                if button.is_clicked(mouse_pos) and button.callback:
                    button.callback()

    setting_button.draw(DISPLAYSURF)
    exit_button.draw(DISPLAYSURF)
    DISPLAYSURF.blit(logo_img, (logo_x, logo_y))
    pvai_button.draw(DISPLAYSURF)
    pvp_button.draw(DISPLAYSURF)
    facebook_button.draw(DISPLAYSURF)
    rules_button.draw(DISPLAYSURF)
    github_button.draw(DISPLAYSURF)

    pygame.display.update()
    fpsClock.tick(FPS)
