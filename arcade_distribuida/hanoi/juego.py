# hanoi/juego.py
class Hanoi:
    """
    Lógica para el juego de las Torres de Hanói.
    Mantiene tres pilas y permite mover discos bajo reglas.
    """
    def __init__(self, discos: int = 3):
        # Representar postes como listas: mayor elemento es más grande
        self.discos = discos
        self.postes = [list(range(discos, 0, -1)), [], []]
        self.resuelto = False

    def mover_disco(self, origen: int, destino: int) -> bool:
        """
        Mueve un disco del poste "origen" al "destino". Devuelve True si es válido.
        Origen y destino en {0,1,2}. No permite colocar disco mayor sobre menor.
        """
        if not self.postes[origen]:
            return False
        disco = self.postes[origen][-1]
        # si destino vacío o disco más pequeño
        if not self.postes[destino] or self.postes[destino][-1] > disco:
            self.postes[origen].pop()
            self.postes[destino].append(disco)
            # comprobar si resuelto: todos en poste 2 o 1
            if len(self.postes[2]) == self.discos or len(self.postes[1]) == self.discos:
                self.resuelto = True
            return True
        return False

    def estado(self) -> list:
        """
        Devuelve una copia de los postes para dibujar la GUI.
        """
        return [list(p) for p in self.postes]
