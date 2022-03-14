from logica.jugadores import Jugador, JugadorBase, Oponente
from typing import Dict
from logica.tablero import ResultadoAtaque, Tablero
import random
from logica.barco import Barco, Crucero, Destructor, Portaaviones, Submarino

if __name__ == "__main__":
    size = 0
    
    while size < 5:
        size = int(input("Ingrese el tamaño del tablero de juego. Debe ser > 5: "))

    numBarcos: Dict[str, int] = {
        "Submarino": int(input("Ingrese el número de submarinos: ")),
        "Destructor": int(input("Ingrese el número de destructores: ")),
        "Crucero": int(input("Ingrese el número de cruceros: ")),
        "Portaaviones": int(input("Ingrese el número de portaaviones: "))
    }

    generarBarcos = lambda: [Barco.getInstance(barco) for barco in numBarcos for i in range(numBarcos[barco])]
    jugador = Jugador(Tablero(size, False), generarBarcos())
    oponente = Oponente(Tablero(size), generarBarcos())
    jugador.getTablero().print()
    
    jugador.ubicar()
    oponente.ubicar()
    ganador: JugadorBase = None
    jugando = jugador if random.random() > 0.5 else oponente
    esperando = jugador if jugando is oponente else oponente

    while not ganador:
        print("Tu turno") if jugando is jugador else print("Turno del oponente")
        resultado = ResultadoAtaque.IMPACTO

        while True:
            resultado = jugando.atacar(esperando)

            for tablero1, tablero2 in zip(jugador.getTablero().toString(), oponente.getTablero().toString()):
                print(tablero1, tablero2, sep=" ")

            if resultado == ResultadoAtaque.FALLO:
                print("Fallo")
                break
            
            if resultado == ResultadoAtaque.IMPACTO:
                print("Impacto, ataca nuevamente")
            
            if resultado == ResultadoAtaque.DESTRUIDO:
                if esperando.perdio():
                    ganador = jugando
                    print("Barco destruido")

                    break
                
                print("Barco destruido, ataca nuevamente")

        temp = jugando
        jugando = esperando
        esperando = temp

    print("Ganaste") if ganador is jugador else print("Perdiste")