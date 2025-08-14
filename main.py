# main.py
import pygame
from ui.main_menu import MainMenu

def run():
    pygame.init()
    screen = pygame.display.set_mode((550, 900))
    pygame.display.set_caption("Cờ Tướng AI")
    clock = pygame.time.Clock()

    menu = MainMenu(screen)
    current_screen = "menu"

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if current_screen == "menu":
                result = menu.handle_event(event)
                if result == "play_ai":
                    current_screen = "ai_game"
                    # TODO: khởi tạo game đấu AI
                elif result == "play_pvp":
                    current_screen = "pvp_game"
                    # TODO: khởi tạo game hai người

        if current_screen == "menu":
            menu.draw()
        else:
            # TODO: vẽ màn hình trò chơi sau khi vào trận
            pass

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    run()