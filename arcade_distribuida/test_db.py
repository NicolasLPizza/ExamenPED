import sqlite3
import pprint

DB_PATH = 'servidor/resultados.db'

def listar_tablas(conn):
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tablas = [row[0] for row in cursor.fetchall()]
    return tablas


def mostrar_contenido(conn, tabla):
    cursor = conn.execute(f"SELECT * FROM {tabla}")
    rows = cursor.fetchall()
    print(f"\n=== Contenido de la tabla '{tabla}' ===")
    for row in rows:
        pprint.pprint(row)


def main():
    conn = sqlite3.connect(DB_PATH)
    try:
        tablas = listar_tablas(conn)
        print("Tablas en la base de datos:", tablas)
        for tabla in tablas:
            mostrar_contenido(conn, tabla)
    finally:
        conn.close()

if __name__ == '__main__':
    main()