# ui/main_menu.py
import pygame

class MainMenu:
    def __init__(self, screen):
        self.screen = screen




    def draw(self):

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btn_ai_rect.collidepoint(event.pos):
                return "play_ai"
                return "play_pvp"
        return None
