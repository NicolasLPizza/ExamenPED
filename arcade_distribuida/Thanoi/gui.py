import threading
from cliente_comun.comunicaciones import ClienteServidor

def enviar_resultado(juego: str, datos: dict):
    """
    Construye el mensaje y lo envía al servidor en un hilo aparte.

    juego: 'nreinas', 'caballo' o 'hanoi'
    datos: diccionario específico de cada juego
    """
    mensaje = {"juego": juego, "accion": "resultado", "datos": datos}

    def _worker(msg):
        client = ClienteServidor()
        try:
            client.conectar()
            client.enviar(msg)
            resp = client.recibir()
            print(f"Servidor respondió ({juego}): {resp}")
        except Exception as e:
            print(f"Error enviando resultado de {juego}: {e}")
        finally:
            client.cerrar()

    threading.Thread(target=_worker, args=(mensaje,), daemon=True).start()


# 2) Integración en nreinas/gui.py
# Coloca este bloque justo cuando detectas fin de partida:

# Variables de tu lógica de juego:
#   tablero_N: int
#   partida_resuelta: bool
#   total_intentos: int

datos_hanoi = {
    "discos": numero_discos,
    "movimientos": movimientos_hechos,
    "resuelto": hanoi_exito
}
enviar_resultado('hanoi', datos_hanoi)
