from __future__ import annotations
from typing import Dict, Generator
from typing import List, Set, Tuple
from random import randint, random


"""Lee el tamaño del tablero de juego y lo inicializa"""
size = int(input("Digite el tamaño del tablero de juego: "))


"""
El tablero de juego, en cada juego se tienen 2 instancias de estos. Una para cada jugador.

Atributos:
celdas -- Matriz cuadrada que contiene a todas las celdas que hacen parte del tablero con tamaño size x size
size -- Tamaño del tablero
hidden -- Booleano que si está activado no permite que se vean los barcos en el tablero.
Por defecto para el jugador es Falso y para la computadora es Verdadero
"""
class Tablero:
    _celdas: List[List[Barco]]
    _barcos: List[Barco]
    _size: int

    def __init__(self, size: int) -> None:
        self._size = size
        self._celdas = [[None for j in range(size)] for i in range(size)]
        self._barcos = []

    """Getters"""
    def getSize(self) -> int:
        return self._size

    def getCeldas(self) -> List[List[Barco]]:
        return self._celdas
        
    """
    Ubica un barco en el tablero basado en los atributos de ese barco.
    Arroja distintos errores si el barco no se puede ubicar correctamente:

    BaseException si el barco no está definido o no ha sido ubicado.
    IndexError si la posición del barco se sale de los límites del tablero.
    ValueError si el barco se está posicionando sobre otro barco.
    """
    def ubicar(self, barco: Barco) -> bool:
        memoria: Set[Tuple[int, int]] = set()
        vertical = random() > 0.5

        for i in range(2):
            for j in range(10000):
                if vertical:
                    x = randint(0, self._size - 1)
                    y = randint(0, self._size - barco.getSize() - 1)
                    
                    if (x, y) in memoria:
                        continue

                    memoria.add((x, y))
                    fueraDelTablero = x >= self._size or x < 0 or y >= self._size - barco.getSize() or y < 0

                    if fueraDelTablero or not self.puedePosicionarse(barco, x, y, vertical):
                        continue

                    for yi in range(y, y + barco.getSize()):
                        self._celdas[yi][x] = barco
                else:
                    x = randint(0, self._size - barco.getSize() - 1)
                    y = randint(0, self._size - 1)
                    
                    if (x, y) in memoria:
                        continue

                    memoria.add((x, y))
                    fueraDelTablero = x >= self._size - barco.getSize() or x < 0 or y >= self._size or y < 0

                    if fueraDelTablero or not self.puedePosicionarse(barco, x, y, vertical):
                        continue

                    for xi in range(x, x + barco.getSize()):
                        self._celdas[y][xi] = barco

                self._barcos.append(barco)
                return True
            
            memoria.clear()
            vertical = not vertical

        return False

    def puedePosicionarse(self, barco: Barco, x: int, y: int, vertical: bool) -> bool:
        if vertical:
            for yi in range(y, y + barco.getSize()):
                if self._celdas[yi][x]:
                    return False
        else:
            for xi in range(x, x + barco.getSize()):
                if self._celdas[y][xi]:
                    return False

        return True

    def __str__(self) -> str:
        return "\n".join([row for row in self.toString()])

    def toString(self) -> Generator[str, None, None]:
        yield "---".join(["+" for i in range(self._size + 1)])
        
        for i in range(self._size):
            row = "|"

            for j in range(self._size):
                barco = self._celdas[i][j]
                content = str(barco.getId()) if barco else " "
                row += f"{content.center(3)}|"

            yield row
            yield "---".join(["+" for i in range(self._size + 1)])


"""
Se inicializa el tablero
"""
tablero = Tablero(size)


class Barco:
    secuencia_id = 0
    
    _id: int
    _name: str
    _size: int

    """
    La clase barco se utilizará para crear cada uno de ellos.
    Parámetros:
    - id: Número que identifica al Barco.
    - nombre: Nombre asignado al Barco.
    - tamaño: Cantidad de bloques que ocupa el barco en el tablero.
    Debe verificar que no sobrepase las dimensiones especificadas.
    """
    def __init__(self, nombre : str, size : int):
        self._name = nombre
        self._size = size
        self._id = Barco.secuencia_id
        Barco.secuencia_id += 1
    
    def getNombre(self) -> str:
        return self._name
    
    def getSize(self) -> int:
        return self._size

    def getId(self) -> int:
        return self._id

    def ubicar(self) -> bool:
        # Método utilizado para ubicar el en el tablero.
        return tablero.ubicar(self)

    def generar(nombre: str) -> Barco:
        if nombre == "Submarino":
            return Barco("Submarino", 1)

        if nombre == "Destructor":
            return Barco("Destructor", 2)

        if nombre == "Crucero":
            return Barco("Crucero", 3)

        if nombre == "Portaaviones":
            return Barco("Portaaviones", 4)


if __name__ == "__main__":
    """Lee el número de los distintos barcos que tendrá el juego"""
    numBarcos: Dict[str, int] = {
        "Submarino": int(input("Ingrese el número de submarinos: ")),
        "Destructor": int(input("Ingrese el número de destructores: ")),
        "Crucero": int(input("Ingrese el número de cruceros: ")),
        "Portaaviones": int(input("Ingrese el número de portaaviones: "))
    }


    """Genera los barcos para un jugador dependiendo del anterior diccionario"""
    barcos = [Barco.generar(barco) for barco in numBarcos for i in range(numBarcos[barco])]
    
    for barco in barcos:
        if barco.getSize() > size:
            raise Exception(f"El barco {barco.getNombre()} {barco.getId()} tiene un tamaño mayor al del tablero, no se puede posicionar.")

        if not barco.ubicar():
            raise Exception("No se pudo ubicar el barco en el tablero, probablemente no hay más espacio.")

    print(tablero)