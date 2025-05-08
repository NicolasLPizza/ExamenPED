# Máquina Arcade Distribuida

Una colección de tres puzzles clásicos solucionados en Python con arquitectura cliente‑servidor, GUI interactivas y almacenamiento de resultados.

## Descripción general

* **Juegos**: N‑Reinas, Knight’s Tour y Torres de Hanói.
* **Cliente‑Servidor**: Cada juego funciona como cliente TCP que envía resultados al servidor central.
* **Interfaz**: Ventanas Pygame para cada juego y un menú principal.
* **Persistencia**: SQLite + SQLAlchemy en el servidor.
* **Comunicación**: JSON sobre sockets, con capa común en `cliente_comun/`.

## Estructura del proyecto

```text
arcade_distribuida/
├── servidor/                 # Servidor central
│   ├── comunicaciones.py     # Servidor multihilo
│   ├── modelos.py            # ORM SQLAlchemy
│   └── config.py             # HOST, PORT
├── cliente_comun/            # Capa de comunicaciones
│   ├── comunicaciones.py
│   ├── utils.py              # enviar_resultado
│   └── config.py
├── nreinas/                  # N‑Reinas
│   ├── juego.py              # Lógica
│   └── gui.py                # GUI Pygame
├── caballo/                  # Knight’s Tour
│   ├── juego.py
│   └── gui.py
├── hanoi/                    # Torres de Hanói
│   ├── juego.py
│   └── gui.py
├── menu.py                   # Menú con test servidor/BD
├── test_cliente.py           # Test N‑Reinas
├── test_envio_juegos.py      # Test Caballo y Hanói
├── test_db.py                # Inspección BD
├── requirements.txt          # Dependencias
└── README.md                 # (este archivo)
```

## Mapeo de requisitos

| Requisito           | Implementación                               |
| ------------------- | -------------------------------------------- |
| Cliente‑Servidor    | `servidor/` y `cliente_comun/`               |
| POO                 | Clases en `juego.py` de cada juego           |
| Concurrencia        | Hilos en servidor y en envío de clientes     |
| GUI                 | Pygame en `*.gui.py` y en `menu.py`          |
| Persistencia        | SQLAlchemy + SQLite en `servidor/modelos.py` |
| Modularidad         | Paquetes `nreinas/`, `caballo/`, `hanoi/`    |
| Fin automático      | Detección de victoria o dead‑end en GUIs     |
| Pruebas             | `test_*.py` scripts                          |
| Verificación rápida | Botones de test en `menu.py`                 |

## Cumplimiento de puntos del profesor

A continuación se detalla cómo y dónde se cumplen los apartados solicitados por la cátedra:

1. **Arquitectura cliente-servidor**

   * Implementado en `servidor/comunicaciones.py` y `cliente_comun/comunicaciones.py`.

2. **Programación Orientada a Objetos (POO)**

   * Clases `Tablero` (`nreinas/juego.py`), `KnightTour` (`caballo/juego.py`) y `Hanoi` (`hanoi/juego.py`).

3. **Concurrencia con hilos**

   * Servidor multihilo en `servidor/comunicaciones.py`.
   * Envío asíncrono en clientes en `cliente_comun/utils.py` y GUIs (`*.gui.py`).

4. **Interfaces gráficas (GUI)**

   * Pygame en `nreinas/gui.py`, `caballo/gui.py`, `hanoi/gui.py` y `menu.py`.

5. **Persistencia de datos (ORM y BD)**

   * Modelos SQLAlchemy en `servidor/modelos.py`.
   * Base de datos SQLite `resultados.db`.

6. **Separación modular**

   * Paquetes independientes `nreinas/`, `caballo/`, `hanoi/` y módulo común `cliente_comun/`.

7. **Detección de final de juego**

   * Lógica de comprobación y mensajes en cada `*.gui.py` (vía `completado` y detección de dead-end).

8. **Menú de comprobaciones**

   * Botones “Probar Servidor” y “Comprobar BD” en `menu.py` para verificación rápida.

9. **Scripts de prueba**

   * `test_cliente.py`, `test_envio_juegos.py` y `test_db.py` para validar comunicación y persistencia.

Con este apartado, queda claro dónde se implementa cada requisito de la práctica.

