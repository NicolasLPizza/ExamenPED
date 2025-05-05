# caballo/juego.py
class KnightTour:
    """
    Lógica para el Knight's Tour (Recorrido del Caballo).
    Lleva registro de la ruta del caballo y permite moverlo.
    """
    MOVIMIENTOS = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                   (1, -2), (1, 2), (2, -1), (2, 1)]

    def __init__(self, N: int = 8):
        self.N = N
        self.origen = None       # posición inicial (fila, col)
        self.recorrido = []      # lista de posiciones visitadas

    def mover(self, pos: tuple) -> bool:
        """
        Intenta mover el caballo a la posición pos (fila, col).
        Si es la primera jugada, establece origen.
        Solo permite movimientos en L y no repetir casilla.
        Devuelve True si el movimiento es válido.
        """
        fila, col = pos
        # compruebo dentro del tablero
        if not (0 <= fila < self.N and 0 <= col < self.N):
            return False
        # primer movimiento
        if not self.recorrido:
            self.origen = pos
            self.recorrido.append(pos)
            return True
        # no repetir casilla
        if pos in self.recorrido:
            return False
        # verificar salto en L
        last = self.recorrido[-1]
        df = abs(last[0] - fila)
        dc = abs(last[1] - col)
        if (df, dc) not in [(1,2), (2,1)]:
            return False
        self.recorrido.append(pos)
        return True

    def completado(self) -> bool:
        """
        True si ha visitado todas las N*N casillas.
        """
        return len(self.recorrido) == self.N * self.N
