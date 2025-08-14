# ui/main_menu.py
import pygame

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        w, h = screen.get_size()

        # Load hình ảnh
        self.background = pygame.image.load("assets/ui/background.png").convert()
        self.logo = pygame.image.load("assets/ui/logo.png").convert_alpha()
        self.btn_ai = pygame.image.load("assets/ui/btn_ai.png").convert_alpha()
        self.btn_pvp = pygame.image.load("assets/ui/btn_pvp.png").convert_alpha()
        self.icon_facebook = pygame.image.load("assets/ui/icon_facebook.png").convert_alpha()
        self.icon_rules = pygame.image.load("assets/ui/icon_rules.png").convert_alpha()
        self.icon_github = pygame.image.load("assets/ui/icon_github.png").convert_alpha()

        # Định vị trí logo và các nút
        self.logo_rect = self.logo.get_rect(center=(w//2, h//4))
        btn_width, btn_height = self.btn_ai.get_size()
        self.btn_ai_rect = self.btn_ai.get_rect(center=(w//2, h//2 - btn_height//1.5))
        self.btn_pvp_rect = self.btn_pvp.get_rect(center=(w//2, h//2 + btn_height//1.5))

        # Định vị trí ba biểu tượng dưới cùng
        icon_size = self.icon_facebook.get_size()
        margin = 80  # khoảng cách giữa các icon
        y_pos = h - icon_size[1] - 40
        self.icon_facebook_rect = self.icon_facebook.get_rect(center=(w//2 - margin, y_pos))
        self.icon_rules_rect = self.icon_rules.get_rect(center=(w//2, y_pos))
        self.icon_github_rect = self.icon_github.get_rect(center=(w//2 + margin, y_pos))

    def draw(self):
        # Vẽ tất cả lên màn hình
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.logo, self.logo_rect)
        self.screen.blit(self.btn_ai, self.btn_ai_rect)
        self.screen.blit(self.btn_pvp, self.btn_pvp_rect)
        self.screen.blit(self.icon_facebook, self.icon_facebook_rect)
        self.screen.blit(self.icon_rules, self.icon_rules_rect)
        self.screen.blit(self.icon_github, self.icon_github_rect)

    def handle_event(self, event):
        # Kiểm tra click chuột
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btn_ai_rect.collidepoint(event.pos):
                print("Bắt đầu chế độ chơi với máy")
                return "play_ai"
            elif self.btn_pvp_rect.collidepoint(event.pos):
                print("Bắt đầu chế độ hai người chơi")
                return "play_pvp"
            elif self.icon_facebook_rect.collidepoint(event.pos):
                print("Mở fanpage…")
            elif self.icon_rules_rect.collidepoint(event.pos):
                print("Mở luật/hướng dẫn…")
            elif self.icon_github_rect.collidepoint(event.pos):
                print("Github")
        return None
