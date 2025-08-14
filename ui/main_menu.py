# ui/main_menu.py
import pygame
import os

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()

        # Đường dẫn tài nguyên
        def load_img(name):
            path = os.path.join("assets/ui", name)
            return pygame.image.load(path).convert_alpha()

        # Nạp ảnh (bạn cần cung cấp đủ các file này)
        self.setting     = load_img("btn_setting.png")       # nút bánh răng (trái)
        self.exit      = load_img("btn_exit.png")        # nút file luật (phải)
        self.logo     = load_img("logo.png")       # logo “Cờ Tướng”
        self.pvai   = load_img("btn_ai.png")     # nút “Chơi Với Máy”
        self.pvp  = load_img("btn_pvp.png")    # nút “Hai Người Chơi”
        self.fb       = load_img("icon_facebook.png")   # biểu tượng fanpage
        self.rules    = load_img("icon_rules.png")      # biểu tượng hướng dẫn
        self.github   = load_img("icon_github.png")     # biểu tượng GitHub/game khác

        # Lấy kích thước từng ảnh
        gw, gh = self.setting.get_size()
        dw, dh = self.exit.get_size()
        lw, lh = self.logo.get_size()
        aiw, aih = self.pvai.get_size()
        pvpw, pvph = self.pvp.get_size()
        fbw, fbh = self.fb.get_size()
        rw, rh = self.rules.get_size()
        gw2, gh2 = self.github.get_size()

        # Các hằng số khoảng cách theo yêu cầu
        MARGIN_TOP = 35
        SPACING_TOP_ICONS = 494    # khoảng cách ngang giữa 2 icon trên cùng (tính theo mép trái)
        SPACING_LOGO_TOP = 35      # khoảng cách dọc giữa icon trên cùng và logo
        SPACING_LOGO_AI = 90       # khoảng cách dọc giữa logo và nút “Chơi Với Máy”
        SPACING_AI_PVP = 67        # khoảng cách dọc giữa 2 nút chơi
        SPACING_PVP_BOTTOM = 130   # khoảng cách dọc giữa nút PVP và hàng icon cuối
        SPACING_BOTTOM_ICONS = 90  # khoảng cách ngang giữa các icon cuối

        # Tính vị trí các icon trên cùng
        setting_left = MARGIN_TOP
        setting_top = MARGIN_TOP
        doc_left = setting_left + gw + SPACING_TOP_ICONS
        doc_top = MARGIN_TOP

        # Tính vị trí logo (đặt giữa theo chiều ngang, cách icon trên 35px)
        logo_left = (self.width - lw) // 2
        logo_top = MARGIN_TOP + gh + SPACING_LOGO_TOP

        # Tính vị trí nút “Chơi Với Máy” (căn ngang giữa, cách logo 90px)
        btn_ai_left = (self.width - aiw) // 2
        btn_ai_top = logo_top + lh + SPACING_LOGO_AI

        # Tính vị trí nút “Hai Người Chơi” (căn ngang giữa, cách nút AI 67px)
        btn_pvp_left = (self.width - pvpw) // 2
        btn_pvp_top = btn_ai_top + aih + SPACING_AI_PVP

        # Tính vị trí 3 icon cuối (căn giữa theo tổng chiều rộng và cách nút PVP 130px)
        # Tổng chiều rộng = 3*icon_width + 2*spacing
        icon_group_width = fbw + SPACING_BOTTOM_ICONS + rw + SPACING_BOTTOM_ICONS + gw2
        group_left = (self.width - icon_group_width) // 2
        icons_top = btn_pvp_top + pvph + SPACING_PVP_BOTTOM

        fb_left = group_left
        rules_left = fb_left + fbw + SPACING_BOTTOM_ICONS
        github_left = rules_left + rw + SPACING_BOTTOM_ICONS

        # Tạo rect để thuận tiện xử lý sự kiện
        self.setting_rect = pygame.Rect(setting_left, setting_top, gw, gh)
        self.doc_rect = pygame.Rect(doc_left, doc_top, dw, dh)
        self.logo_rect = pygame.Rect(logo_left, logo_top, lw, lh)
        self.btn_ai_rect = pygame.Rect(btn_ai_left, btn_ai_top, aiw, aih)
        self.btn_pvp_rect = pygame.Rect(btn_pvp_left, btn_pvp_top, pvpw, pvph)
        self.fb_rect = pygame.Rect(fb_left, icons_top, fbw, fbh)
        self.rules_rect = pygame.Rect(rules_left, icons_top, rw, rh)
        self.github_rect = pygame.Rect(github_left, icons_top, gw2, gh2)

    def draw(self):
        # Màu nền nâu hoặc load ảnh nền riêng nếu có
        self.screen.fill((138, 92, 60))
        # Vẽ từng phần tử lên màn hình
        self.screen.blit(self.setting, self.setting_rect.topleft)
        self.screen.blit(self.exit, self.doc_rect.topleft)
        self.screen.blit(self.logo, self.logo_rect.topleft)
        self.screen.blit(self.pvai, self.btn_ai_rect.topleft)
        self.screen.blit(self.pvp, self.btn_pvp_rect.topleft)
        self.screen.blit(self.fb, self.fb_rect.topleft)
        self.screen.blit(self.rules, self.rules_rect.topleft)
        self.screen.blit(self.github, self.github_rect.topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btn_ai_rect.collidepoint(event.pos):
                return "play_ai"
            if self.btn_pvp_rect.collidepoint(event.pos):
                return "play_pvp"
        return None
