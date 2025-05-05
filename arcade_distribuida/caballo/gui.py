# caballo/gui.py
import threading
import pygame
from cliente_comun.utils import enviar_resultado
from caballo.juego import KnightTour  # tu clase Knight’s Tour

class KnightTourGUI:
    def __init__(self, N=8):
        pygame.init()
        self.N = N
        self.tour = KnightTour(N)
        self.saltos = 0
        self.completo = False
        self.size = 600
        self.screen = pygame.display.set_mode((self.size, self.size))
        pygame.display.set_caption("Knight's Tour")
        self.cell = self.size // N

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.completo:
                    col, fila = event.pos[0]//self.cell, event.pos[1]//self.cell
                    if self.tour.mover((fila, col)):
                        self.saltos += 1
                        if self.tour.completado():
                            self.completo = True
                            threading.Thread(
                                target=lambda: enviar_resultado('caballo', {
                                    'posicion_inicial': self.tour.origen,
                                    'movimientos': self.saltos,
                                    'completado': True
                                }),
                                daemon=True
                            ).start()
            self._draw()
        pygame.quit()

    def _draw(self):
        self.screen.fill((255,255,255))
        # dibuja tablero y camino...
        pygame.display.flip()

if __name__ == '__main__':
    gui = KnightTourGUI()
    gui.run()
