# menu.py
"""
Menú principal con Pygame para seleccionar uno de los tres juegos:
- N-Reinas
- Knight's Tour
- Torres de Hanói
Al hacer clic en un botón, se lanza el juego correspondiente en un nuevo proceso.
"""
import pygame
import sys
import subprocess
import os

# Configuración
WIDTH, HEIGHT = 400, 300
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
BUTTON_MARGIN = 20
BACKGROUND_COLOR = (30, 30, 30)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HIGHLIGHT = (100, 160, 210)
TEXT_COLOR = (255, 255, 255)
FONT_SIZE = 24

GAMES = [
    ("N-Reinas", [sys.executable, "-m", "nreinas.gui"]),
    ("Knight's Tour", [sys.executable, "-m", "caballo.gui"]),
    ("Torres de Hanói", [sys.executable, "-m", "hanoi.gui"]),
]

class Button:
    def __init__(self, text, rect, command):
        self.text = text
        self.rect = pygame.Rect(rect)
        self.command = command
        self.hover = False

    def draw(self, surface, font):
        color = BUTTON_HIGHLIGHT if self.hover else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect)
        text_surf = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.hover:
            self.command()


def launch_game(cmd):
    try:
        # Lanzar en nuevo proceso
        subprocess.Popen(cmd)
    except Exception as e:
        print(f"Error al lanzar juego: {e}")


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Máquina Arcade - Menú")
    font = pygame.font.Font(None, FONT_SIZE)

    buttons = []
    total_height = len(GAMES) * BUTTON_HEIGHT + (len(GAMES) - 1) * BUTTON_MARGIN
    start_y = (HEIGHT - total_height) // 2

    for i, (label, cmd) in enumerate(GAMES):
        x = (WIDTH - BUTTON_WIDTH) // 2
        y = start_y + i * (BUTTON_HEIGHT + BUTTON_MARGIN)
        buttons.append(Button(label, (x, y, BUTTON_WIDTH, BUTTON_HEIGHT),
                              lambda c=cmd: launch_game(c)))

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for btn in buttons:
                btn.handle_event(event)

        screen.fill(BACKGROUND_COLOR)
        for btn in buttons:
            btn.draw(screen, font)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    # Ajustar path de trabajo a la carpeta del script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
