import threading
import pygame
from cliente_comun.utils import enviar_resultado
from hanoi.juego import Hanoi
import sys

WINDOW_SIZE = 600
BG_COLOR = (255,255,255)
PEG_COLOR = (139,69,19)
DISC_COLOR = (0,128,0)
FONT_SIZE = 32

# pide número de discos antes de iniciar
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
        txt = font.render(f"{prompt}: {input_str}", True, (0,0,0))
        screen.blit(txt, (10,30))
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
    return int(input_str) if input_str.isdigit() else None

class HanoiGUI:
    def __init__(self, discos):
        pygame.init()
        self.discos = discos
        self.hanoi = Hanoi(discos)
        self.movimientos = 0
        self.exito = False
        self.size = WINDOW_SIZE
        self.screen = pygame.display.set_mode((self.size, self.size))
        pygame.display.set_caption("Torres de Hanói")
        self.peg_x = [self.size//6, self.size//2, 5*self.size//6]
        self.peg_width = self.size//12
        self.selected = None
        self.font = pygame.font.Font(None, FONT_SIZE)

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.exito:
                    x, y = event.pos
                    for i, px in enumerate(self.peg_x):
                        if abs(x-px) < self.peg_width*2:
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
                                        }), daemon=True
                                    ).start()
                            break
            self._draw()
            if self.exito:
                pygame.time.delay(2000)
                running = False
            clock.tick(30)
        pygame.quit()
        sys.exit()

    def _draw(self):
        self.screen.fill(BG_COLOR)
        for px in self.peg_x:
            pygame.draw.rect(self.screen, PEG_COLOR,
                             (px-self.peg_width//2, self.size//4,
                              self.peg_width, self.size//2))
        level_h = (self.size//2)//self.discos
        for i, stack in enumerate(self.hanoi.postes):
            for depth, disc in enumerate(stack):
                w = disc*self.peg_width
                x = self.peg_x[i]-w//2
                y = self.size-(depth+1)*level_h
                pygame.draw.rect(self.screen, DISC_COLOR,
                                 (x,y,w,level_h-5))
        if self.selected is not None:
            px = self.peg_x[self.selected]
            pygame.draw.circle(self.screen, (255,0,0), (px,self.size//8), self.peg_width//2, 3)
        if self.exito:
            text = self.font.render("¡Victoria!", True, (0,0,0))
            self.screen.blit(text, (10,10))
        pygame.display.flip()

if __name__ == '__main__':
    discos = get_number_input("Número de discos")
    if discos and discos>0:
        gui = HanoiGUI(discos)
        gui.run()
