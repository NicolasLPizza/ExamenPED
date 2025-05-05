# test_envio_juegos.py
# Script para enviar datos de prueba de "caballo" y "hanoi" al servidor.

from cliente_comun.config import HOST, PORT
from cliente_comun.comunicaciones import ClienteServidor
import json
import socket


def enviar_test(juego: str, datos: dict):
    mensaje = {"juego": juego, "accion": "resultado", "datos": datos}
    client = ClienteServidor(HOST, PORT)
    try:
        client.conectar()
        print(f"Enviando al servidor ({juego}): {datos}")
        client.enviar(mensaje)
        resp = client.recibir()
        print(f"Respuesta del servidor ({juego}): {resp}\n")
    except Exception as e:
        print(f"Error enviando {juego}: {e}\n")
    finally:
        client.cerrar()


def main():
    # Datos de prueba para Caballo
    datos_caballo = {
        "posicion_inicial": "B1",
        "movimientos": 50,
        "completado": False
    }
    # Datos de prueba para Hanói
    datos_hanoi = {
        "discos": 4,
        "movimientos": 15,
        "resuelto": False
    }

    enviar_test('caballo', datos_caballo)
    enviar_test('hanoi', datos_hanoi)

if __name__ == '__main__':
    main()