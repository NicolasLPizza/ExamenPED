# nreinas/juego.py
class Tablero:
    """
    Lógica para el puzzle de las N-Reinas.
    Mantiene una lista de posiciones de reinas (fila, col) y verifica
    las reglas de ataque.
    """
    def __init__(self, N: int):
        self.N = N
        self.reinas = []  # lista de tuplas (fila, col)

    def es_valido(self, fila: int, col: int) -> bool:
        """
        Devuelve True si colocar una reina en (fila, col) no es atacada
        por ninguna reina ya en self.reinas.
        """
        for r, c in self.reinas:
            # misma fila o columna
            if r == fila or c == col:
                return False
            # misma diagonal
            if abs(r - fila) == abs(c - col):
                return False
        return True

    def colocar_reina(self, fila: int, col: int) -> bool:
        """
        Intenta colocar una reina en (fila,col). Si es válido, la añade
        a la lista y devuelve True; en caso contrario, devuelve False.
        """
        if self.es_valido(fila, col):
            self.reinas.append((fila, col))
            return True
        return False

    def completado(self) -> bool:
        """
        Retorna True si ya se han colocado N reinas.
        """
        return len(self.reinas) == self.N
