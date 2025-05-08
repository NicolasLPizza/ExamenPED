# nreinas/gui.py
import threading
import pygame
from cliente_comun.utils import enviar_resultado
from nreinas.juego import Tablero
import sys

WINDOW_SIZE = 600
BG_COLOR = (200, 200, 200)
LINE_COLOR = (0, 0, 0)
FONT_COLOR = (0, 0, 0)
FONT_SIZE = 32

class NReinasGUI:
    def __init__(self, N):
        pygame.init()
        self.N = N
        self.tablero = Tablero(N)
        self.intentos = 0
        self.exito = False
        self.size = WINDOW_SIZE
        self.screen = pygame.display.set_mode((self.size, self.size))
        pygame.display.set_caption(f"N-Reinas (N={N})")
        self.cell = self.size // N
        self.font = pygame.font.Font(None, FONT_SIZE)

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            moved = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.exito:
                    x, y = event.pos
                    fila, col = y // self.cell, x // self.cell
                    if self.tablero.colocar_reina(fila, col):
                        self.intentos += 1
                        moved = True
                        if self.tablero.completado():
                            self.exito = True
                            threading.Thread(
                                target=lambda: enviar_resultado('nreinas', {
                                    'N': self.N,
                                    'resuelto': True,
                                    'movimientos': self.intentos
                                }), daemon=True
                            ).start()
                        else:
                            # verificar si quedan movimientos válidos
                            any_valid = any(
                                self.tablero.es_valido(r, c)
                                for r in range(self.N)
                                for c in range(self.N)
                                if (r, c) not in self.tablero.reinas
                            )
                            if not any_valid:
                                self.exito = True
                                self.victory_msg = "¡Enhorabuena, no hay más opciones!"
                                threading.Thread(
                                    target=lambda: enviar_resultado('nreinas', {
                                        'N': self.N,
                                        'resuelto': False,
                                        'movimientos': self.intentos
                                    }), daemon=True
                                ).start()
            self._draw()
            if self.exito:
                # mostrar mensaje y salir tras breve espera
                pygame.time.delay(2000)
                running = False
            clock.tick(30)
        pygame.quit()
        sys.exit()

    def _draw(self):
        self.screen.fill(BG_COLOR)
        for i in range(self.N + 1):
            pygame.draw.line(self.screen, LINE_COLOR, (i * self.cell, 0), (i * self.cell, self.size))
            pygame.draw.line(self.screen, LINE_COLOR, (0, i * self.cell), (self.size, i * self.cell))
        for (r, c) in self.tablero.reinas:
            pygame.draw.circle(
                self.screen,
                (200, 0, 0),
                (c * self.cell + self.cell // 2, r * self.cell + self.cell // 2),
                self.cell // 3
            )
        if self.exito:
            msg = getattr(self, 'victory_msg', '¡Resuelto!')
            text = self.font.render(msg, True, FONT_COLOR)
            self.screen.blit(text, (10, 10))
        pygame.display.flip()


def get_number_input(prompt):
    pygame.init()
    width, height = 400, 100
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(prompt)
    font = pygame.font.Font(None, FONT_SIZE)
    input_str = ''
    clock = pygame.time.Clock()
    active = True
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    input_str = input_str[:-1]
                elif event.unicode.isdigit():
                    input_str += event.unicode
        screen.fill(BG_COLOR)
        txt_surf = font.render(f"{prompt}: {input_str}", True, FONT_COLOR)
        screen.blit(txt_surf, (10, 30))
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
    return int(input_str) if input_str.isdigit() else None

if __name__ == '__main__':
    N = get_number_input("Tamaño del tablero N")
    if N and N > 0:
        gui = NReinasGUI(N)
        gui.run()