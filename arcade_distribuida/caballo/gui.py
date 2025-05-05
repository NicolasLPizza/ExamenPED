# caballo/gui.py
import threading
import pygame
from cliente_comun.utils import enviar_resultado
from caballo.juego import KnightTour

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
                    col, fila = event.pos[0] // self.cell, event.pos[1] // self.cell
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
        # dibujar tablero ajedrez
        for r in range(self.N):
            for c in range(self.N):
                color = (240, 217, 181) if (r + c) % 2 == 0 else (181, 136, 99)
                pygame.draw.rect(
                    self.screen,
                    color,
                    (c * self.cell, r * self.cell, self.cell, self.cell)
                )
        # dibujar recorrido
        for pos in self.tour.recorrido:
            r, c = pos
            pygame.draw.circle(
                self.screen,
                (0, 0, 255),
                (c * self.cell + self.cell // 2, r * self.cell + self.cell // 2),
                self.cell // 6
            )
        # dibujar caballo en la última posición
        if self.tour.recorrido:
            r, c = self.tour.recorrido[-1]
            pygame.draw.circle(
                self.screen,
                (255, 0, 0),
                (c * self.cell + self.cell // 2, r * self.cell + self.cell // 2),
                self.cell // 3
            )
        pygame.display.flip()

if __name__ == '__main__':
    gui = KnightTourGUI()
    gui.run()

# Nota: Este código es un ejemplo básico y puede requerir ajustes según la implementación de la clase KnightTour y el entorno de ejecución.
# Asegúrate de tener pygame instalado y la clase KnightTour correctamente implementada.