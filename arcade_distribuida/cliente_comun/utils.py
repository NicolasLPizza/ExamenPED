# cliente_comun/utils.py
"""
Funciones de utilidad compartidas por los clientes.
"""
import threading
from cliente_comun.comunicaciones import ClienteServidor
import cliente_comun.config as cfg


def enviar_resultado(juego: str, datos: dict):
    """
    Construye el mensaje JSON para el servidor y lo envía en un hilo sin bloquear.

    Args:
        juego: Identificador del juego ('nreinas', 'caballo', 'hanoi').
        datos: Diccionario con los campos específicos de la partida.
    """
    mensaje = {
        "juego": juego,
        "accion": "resultado",
        "datos": datos
    }

    def _worker(msg):
        client = ClienteServidor(cfg.HOST, cfg.PORT)
        try:
            client.conectar()
            client.enviar(msg)
            respuesta = client.recibir()
            print(f"Servidor respondió ({juego}): {respuesta}")
        except Exception as e:
            print(f"Error enviando resultado de {juego}: {e}")
        finally:
            client.cerrar()

    threading.Thread(target=_worker, args=(mensaje,), daemon=True).start()
