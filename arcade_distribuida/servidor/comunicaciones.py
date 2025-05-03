# servidor/comunicaciones.py
import socket
import threading
import json
from servidor.modelos import Session, ResultadoNReinas, ResultadoCaballo, ResultadoHanoi

class ServidorTCP:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        print(f"Servidor TCP escuchando en {self.host}:{self.port}…")

    def iniciar(self):
        try:
            while True:
                conn, addr = self.sock.accept()
                print(f"Conexión entrante desde {addr}")
                threading.Thread(
                    target=self.procesar_cliente,
                    args=(conn, addr),
                    daemon=True
                ).start()
        except KeyboardInterrupt:
            print("Servidor detenido por teclado")
        finally:
            self.sock.close()

    def procesar_cliente(self, conn: socket.socket, addr):
        with conn:
            try:
                # Leer encabezado de longitud (4 bytes)
                raw_len = conn.recv(4)
                if not raw_len:
                    return
                msg_len = int.from_bytes(raw_len, 'big')
                # Leer el mensaje completo
                data = b''
                while len(data) < msg_len:
                    chunk = conn.recv(msg_len - len(data))
                    if not chunk:
                        break
                    data += chunk
                # Decodificar JSON
                mensaje = json.loads(data.decode('utf-8'))
                print(f"[{addr}] Mensaje recibido: {mensaje}")
                # Guardar en BD
                self._guardar_en_bd(mensaje)
                respuesta = {"status": "ok"}
            except Exception as e:
                print(f"Error procesando cliente {addr}: {e}")
                respuesta = {"status": "error", "detail": str(e)}
            # Enviar confirmación
            resp_bytes = json.dumps(respuesta).encode('utf-8')
            conn.sendall(len(resp_bytes).to_bytes(4, 'big') + resp_bytes)

    def _guardar_en_bd(self, msg: dict):
        session = Session()
        juego = msg.get("juego")
        datos = msg.get("datos", {})
        try:
            if juego == "nreinas":
                r = ResultadoNReinas(
                    N=datos["N"],
                    resuelto=datos["resuelto"],
                    movimientos=datos["movimientos"]
                )
                session.add(r)
            elif juego == "caballo":
                r = ResultadoCaballo(
                    posicion_inicial=datos.get("posicion_inicial", ""),
                    movimientos=datos.get("movimientos", 0),
                    completado=datos.get("completado", False)
                )
                session.add(r)
            elif juego == "hanoi":
                r = ResultadoHanoi(
                    discos=datos.get("discos", 0),
                    movimientos=datos.get("movimientos", 0),
                    resuelto=datos.get("resuelto", False)
                )
                session.add(r)
            session.commit()
            print(f"Guardado en BD resultado de {juego}")
        except:
            session.rollback()
            raise
        finally:
            session.close()
