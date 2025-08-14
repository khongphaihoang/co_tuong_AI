import pygame
import pygame_gui
from ui.main_menu import MainMenu

pygame.init()
pygame.display.set_caption("Cờ Tướng AI")

WINDOW_SIZE = (750, 1080)
screen = pygame.display.set_mode(WINDOW_SIZE)
manager = pygame_gui.UIManager(WINDOW_SIZE, theme_path=None)

menu = MainMenu(screen, manager)

clock = pygame.time.Clock()
running = True
while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        manager.process_events(event)

    manager.update(dt)
    menu.draw()
    manager.draw_ui(screen)
    pygame.display.flip()

pygame.quit()
