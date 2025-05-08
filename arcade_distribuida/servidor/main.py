from servidor.modelos import Base, engine
from servidor.comunicaciones import ServidorTCP
import servidor.config as cfg

def main():
    # Crea las tablas si no existen
    Base.metadata.create_all(engine)
    # Arranca el servidor en cfg.HOST:cfg.PORT
    servidor = ServidorTCP(cfg.HOST, cfg.PORT)
    servidor.iniciar()

if __name__ == '__main__':
    main()
