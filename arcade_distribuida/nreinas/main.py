from cliente_comun.comunicaciones import ClienteServidor
import cliente_comun.config as cfg

client = ClienteServidor(cfg.HOST, cfg.PORT)
client.conectar()
resultado = {
    "juego": "nreinas",
    "accion": "resultado",
    "datos": {"N": 8, "resuelto": True, "movimientos": 14}
}
client.enviar(resultado)
# si el servidor responde algo, lo recoges
resp = client.recibir()
print("Respuesta del servidor:", resp)
client.cerrar()
