# hanoi/gui.py
import threading
import pygame
from cliente_comun.utils import enviar_resultado
from hanoi.juego import Hanoi  # tu clase Torres de Hanói

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

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # lógica de arrastrar y soltar discos...
                if self.hanoi.resuelto and not self.exito:
                    self.exito = True
                    threading.Thread(
                        target=lambda: enviar_resultado('hanoi', {
                            'discos': self.discos,
                            'movimientos': self.movimientos,
                            'resuelto': True
                        }),
                        daemon=True
                    ).start()
            self._draw()
        pygame.quit()

    def _draw(self):
        self.screen.fill((255,255,255))
        # dibuja varillas y discos...
        pygame.display.flip()

if __name__ == '__main__':
    discos = int(input("Número de discos: "))
    gui = HanoiGUI(discos)
    gui.run()
