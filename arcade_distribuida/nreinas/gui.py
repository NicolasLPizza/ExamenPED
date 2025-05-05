# nreinas/gui.py
import threading
import pygame
from cliente_comun.utils import enviar_resultado
from nreinas.juego import Tablero  # tu clase de lógica de N-Reinas

class NReinasGUI:
    def __init__(self, N):
        pygame.init()
        self.N = N
        self.tablero = Tablero(N)
        self.intentos = 0
        self.exito = False
        self.size = 600
        self.screen = pygame.display.set_mode((self.size, self.size))
        pygame.display.set_caption(f"N-Reinas (N={N})")
        self.cell = self.size // N

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.exito:
                    x, y = event.pos
                    fila, col = y // self.cell, x // self.cell
                    if self.tablero.colocar_reina(fila, col):
                        self.intentos += 1
                        if self.tablero.completado():
                            self.exito = True
                            threading.Thread(
                                target=lambda: enviar_resultado('nreinas', {
                                    'N': self.N,
                                    'resuelto': True,
                                    'movimientos': self.intentos
                                }),
                                daemon=True
                            ).start()
            self._draw()
        pygame.quit()

    def _draw(self):
        self.screen.fill((255,255,255))
        for i in range(self.N+1):
            pygame.draw.line(self.screen, (0,0,0), (i*self.cell,0), (i*self.cell,self.size))
            pygame.draw.line(self.screen, (0,0,0), (0,i*self.cell), (self.size,i*self.cell))
        for (r,c) in self.tablero.reinas:
            pygame.draw.circle(self.screen, (200,0,0),
                               (c*self.cell + self.cell//2, r*self.cell + self.cell//2),
                               self.cell//3)
        pygame.display.flip()

if __name__ == '__main__':
    N = int(input("Tamaño del tablero N: "))
    gui = NReinasGUI(N)
    gui.run()
