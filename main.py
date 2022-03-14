from logica.jugadores import Jugador, JugadorBase, Oponente
from typing import Dict
from logica.tablero import ResultadoAtaque, Tablero
import random
from logica.barco import Barco

if __name__ == "__main__":
    size = 0
    
    """Lee el tamaño del tablero de juego"""
    while size < 5:
        size = int(input("Ingrese el tamaño del tablero de juego. Debe ser > 5: "))

    """Lee el número de los distintos barcos que tendrá el juego"""
    numBarcos: Dict[str, int] = {
        "Submarino": int(input("Ingrese el número de submarinos: ")),
        "Destructor": int(input("Ingrese el número de destructores: ")),
        "Crucero": int(input("Ingrese el número de cruceros: ")),
        "Portaaviones": int(input("Ingrese el número de portaaviones: "))
    }

    """Genera los barcos para un jugador dependiendo del anterior diccionario"""
    generarBarcos = lambda: [Barco.getInstance(barco) for barco in numBarcos for i in range(numBarcos[barco])]
    
    """Se inicializan los jugadores"""
    jugador = Jugador(Tablero(size, False), generarBarcos())
    oponente = Oponente(Tablero(size), generarBarcos())
    jugador.getTablero().print()
    
    jugador.ubicar()
    oponente.ubicar()
    ganador: JugadorBase = None
    jugando = jugador if random.random() > 0.5 else oponente
    esperando = jugador if jugando is oponente else oponente

    """Mientras que no haya ganado nadie..."""
    while not ganador:
        print("Tu turno") if jugando is jugador else print("Turno del oponente")

        while True:
            """El jugador al cual le pertenezca el turno actual ataca a su oponente"""
            resultado = jugando.atacar(esperando)

            """Se imprimen los tableros"""
            for tablero1, tablero2 in zip(jugador.getTablero().toString(), oponente.getTablero().toString()):
                print(tablero1, tablero2, sep=" ")
                
            if resultado == ResultadoAtaque.FALLO:
                print("Fallo")
                break
            
            """Si impacta a un barco del oponente, el mismo jugador ataca nuevamente"""
            if resultado == ResultadoAtaque.IMPACTO:
                print("Impacto, ataca nuevamente")
            
            if resultado == ResultadoAtaque.DESTRUIDO:
                """Si destruye el último barco del oponente, gana el juego"""
                if esperando.perdio():
                    ganador = jugando
                    print("Barco destruido")

                    break
                
                print("Barco destruido, ataca nuevamente")

        """Si falla el ataque, el turno pasa al otro jugador"""
        temp = jugando
        jugando = esperando
        esperando = temp

    print("Ganaste") if ganador is jugador else print("Perdiste")