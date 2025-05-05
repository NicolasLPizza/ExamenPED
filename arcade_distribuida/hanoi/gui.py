# hanoi/gui.py
import threading
import pygame
from cliente_comun.utils import enviar_resultado
from hanoi.juego import Hanoi

class HanoiGUI:
    def __init__(self, discos=3):
        pygame.init()
        self.discos = discos
        self.hanoi = Hanoi(discos)
        self.movimientos = 0
        self.exito = False
        self.size = 600
        self.screen = pygame.display.set_mode((self.size, self.size))
        pygame.display.set_caption("Torres de Hanói")
        # posiciones centrales de los tres postes
        self.peg_x = [self.size // 6, self.size // 2, 5 * self.size // 6]
        self.peg_width = self.size // 12
        self.selected = None

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.exito:
                    x, y = event.pos
                    # determinar peg pulsado
                    for i, px in enumerate(self.peg_x):
                        if abs(x - px) < self.peg_width * 2:
                            if self.selected is None:
                                self.selected = i
                            else:
                                if self.hanoi.mover_disco(self.selected, i):
                                    self.movimientos += 1
                                self.selected = None
                                if self.hanoi.resuelto:
                                    self.exito = True
                                    threading.Thread(
                                        target=lambda: enviar_resultado('hanoi', {
                                            'discos': self.discos,
                                            'movimientos': self.movimientos,
                                            'resuelto': True
                                        }),
                                        daemon=True
                                    ).start()
                            break
            self._draw()
        pygame.quit()

    def _draw(self):
        self.screen.fill((255, 255, 255))
        # dibujar postes
        for px in self.peg_x:
            pygame.draw.rect(
                self.screen,
                (139, 69, 19),
                (px - self.peg_width // 2, self.size // 4, self.peg_width, self.size // 2)
            )
        # dibujar discos
        level_height = (self.size // 2) // self.discos
        for i, stack in enumerate(self.hanoi.postes):
            for depth, disc in enumerate(stack):
                width = disc * (self.peg_width)
                x = self.peg_x[i] - width // 2
                y = self.size - (depth + 1) * level_height
                pygame.draw.rect(
                    self.screen,
                    (0, 128, 0),
                    (x, y, width, level_height - 5)
                )
        # resaltar selección
        if self.selected is not None:
            px = self.peg_x[self.selected]
            pygame.draw.circle(
                self.screen,
                (255, 0, 0),
                (px, self.size // 8),
                self.peg_width // 2,
                3
            )
        pygame.display.flip()

if __name__ == '__main__':
    discos = int(input("Número de discos: "))
    gui = HanoiGUI(discos)
    gui.run()
