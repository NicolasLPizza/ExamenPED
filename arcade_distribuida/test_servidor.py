# test_servidor.py

import socket


HOST = 'localhost'
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"Echo‑server escuchando en {HOST}:{PORT}…")
    conn, addr = s.accept()
    with conn:
        print('Cliente conectado desde', addr)
        # Leemos el mensaje completo (4 bytes de longitud + payload)
        raw_len = conn.recv(4)
        if not raw_len:
            exit()
        msg_len = int.from_bytes(raw_len, 'big')
        data = conn.recv(msg_len)
        print("Recibido del cliente:", data.decode())
        # Le devolvemos exactamente lo mismo
        conn.sendall(raw_len + data)
        print("Mensaje eco enviado, cerrando conexión.")
