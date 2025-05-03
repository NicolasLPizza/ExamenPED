import socket
import json
import threading

class ClienteServidor:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lock = threading.Lock()    # para proteger envíos concurrentes

    def conectar(self):
        """Conecta al servidor. Lanza excepción si falla."""
        self.sock.connect((self.host, self.port))

    def enviar(self, mensaje: dict):
        """
        Envía un diccionario como JSON:
        - Serializamos con json.dumps
        - Prependemos 4 bytes con la longitud del mensaje (para que el receptor sepa cuántos bytes leer)
        """
        datos = json.dumps(mensaje).encode('utf-8')
        longitud = len(datos).to_bytes(4, byteorder='big')
        with self.lock:
            self.sock.sendall(longitud + datos)

    def recibir(self) -> dict:
        """
        Lee primero 4 bytes de longitud y luego lee exactamente ese número de bytes.
        Convierte de vuelta a dict con json.loads.
        """
        raw_len = self.sock.recv(4)
        if not raw_len:
            return None
        msg_len = int.from_bytes(raw_len, byteorder='big')
        datos = b''
        while len(datos) < msg_len:
            paquete = self.sock.recv(msg_len - len(datos))
            if not paquete:
                break
            datos += paquete
        return json.loads(datos.decode('utf-8'))

    def cerrar(self):
        """Cierra el socket."""
        self.sock.close()
