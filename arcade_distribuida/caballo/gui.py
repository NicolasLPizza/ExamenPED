import threading
import pygame
from cliente_comun.utils import enviar_resultado
from caballo.juego import KnightTour
import sys

WINDOW_SIZE = 600
LIGHT_COLOR = (240, 217, 181)
DARK_COLOR = (181, 136, 99)
PATH_COLOR = (0, 0, 255)
KNIGHT_COLOR = (255, 0, 0)
FONT_SIZE = 32

class KnightTourGUI:
    def __init__(self, N=8):
        pygame.init()
        self.N = N
        self.tour = KnightTour(N)
        self.saltos = 0
        self.completo = False
        self.dead_end = False
        self.size = WINDOW_SIZE
        self.screen = pygame.display.set_mode((self.size, self.size))
        pygame.display.set_caption("Knight's Tour")
        self.cell = self.size // N
        self.font = pygame.font.Font(None, FONT_SIZE)

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not (self.completo or self.dead_end):
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
                                }), daemon=True
                            ).start()
                        else:
                            # verificar posibles siguientes movimientos
                            last = self.tour.recorrido[-1]
                            moves = [(last[0]+dr, last[1]+dc) for dr, dc in KnightTour.MOVIMIENTOS]
                            has_next = any(
                                0 <= r < self.N and 0 <= c < self.N and (r, c) not in self.tour.recorrido
                                and (abs(r-last[0]), abs(c-last[1])) in [(1,2),(2,1)]
                                for r, c in moves
                            )
                            if not has_next:
                                self.dead_end = True
                                threading.Thread(
                                    target=lambda: enviar_resultado('caballo', {
                                        'posicion_inicial': self.tour.origen,
                                        'movimientos': self.saltos,
                                        'completado': False
                                    }), daemon=True
                                ).start()
            self._draw()
            if self.completo or self.dead_end:
                pygame.time.delay(2000)
                running = False
            clock.tick(30)
        pygame.quit()
        sys.exit()

    def _draw(self):
        for r in range(self.N):
            for c in range(self.N):
                color = LIGHT_COLOR if (r + c) % 2 == 0 else DARK_COLOR
                pygame.draw.rect(self.screen, color, (c*self.cell, r*self.cell, self.cell, self.cell))
        # camino recorrido
        for pos in self.tour.recorrido:
            r, c = pos
            pygame.draw.circle(self.screen, PATH_COLOR,
                               (c*self.cell + self.cell//2, r*self.cell + self.cell//2), self.cell//6)
        # dibujo del caballo (punto rojo)
        if self.tour.recorrido:
            r, c = self.tour.recorrido[-1]
            pygame.draw.circle(self.screen, KNIGHT_COLOR,
                               (c*self.cell + self.cell//2, r*self.cell + self.cell//2), self.cell//3)
        # mensaje de victoria o derrota 
        if self.completo or self.dead_end:
            msg = "¡Completado!" if self.completo else "No hay más movimientos"
            text_surf = self.font.render(msg, True, (0,0,0))
            self.screen.blit(text_surf, (10, 10))
        pygame.display.flip()

if __name__ == '__main__':
    gui = KnightTourGUI()
    gui.run()
