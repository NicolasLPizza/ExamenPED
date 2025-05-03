# test_cliente.py

from cliente_comun.comunicaciones import ClienteServidor

if __name__ == '__main__':
    cliente = ClienteServidor('localhost', 5000)
    cliente.conectar()
    mensaje = {
        "juego": "nreinas",
        "accion": "resultado",
        "datos": {"N": 8, "resuelto": True, "movimientos": 14}
    }
    print("Enviando al servidor:", mensaje)
    cliente.enviar(mensaje)

    respuesta = cliente.recibir()
    print("Respuesta del servidor (eco):", respuesta)

    cliente.cerrar()
