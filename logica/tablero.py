from enum import Enum
from logica.barco import Barco
from typing import Generator, List

"""Enum que dice si un ataque falló, impactó a un barco ó destruyó a un barco"""
class ResultadoAtaque(Enum):
    FALLO = 1
    IMPACTO = 2
    DESTRUIDO = 3

"""
Representa una celda dentro de un tablero.

Atributos:
barco -- Si hay un barco que abarca esta celda, se almacena en este campo
hit -- Booleano que es verdadero si la celda ya ha sido impactada
"""
class Celda:
    _barco: Barco
    _hit: bool

    def __init__(self) -> None:
        self._barco = None
        self._hit = False
    
    """Getters y Setters"""
    def setBarco(self, barco: Barco):
        self._barco = barco

    def getBarco(self) -> Barco:
        return self._barco

    def setHit(self):
        self._hit = True

    def getHit(self) -> bool:
        return self._hit


"""
El tablero de juego, en cada juego se tienen 2 instancias de estos. Una para cada jugador.

Atributos:
celdas -- Matriz cuadrada que contiene a todas las celdas que hacen parte del tablero con tamaño size x size
size -- Tamaño del tablero
hidden -- Booleano que si está activado no permite que se vean los barcos en el tablero.
Por defecto para el jugador es Falso y para la computadora es Verdadero
"""
class Tablero:
    _celdas: List[List[Celda]]
    _size: int
    _hidden: bool

    def __init__(self, size: int, hidden: bool = True) -> None:
        self._size = size
        self._celdas = [[Celda() for j in range(size)] for i in range(size)]
        self._hidden = hidden

    """Getters"""
    def getSize(self) -> int:
        return self._size

    def getCells(self) -> List[List[Celda]]:
        return self._celdas

    """
    Ubica un barco en el tablero basado en los atributos de ese barco.
    Arroja distintos errores si el barco no se puede ubicar correctamente:

    BaseException si el barco no está definido o no ha sido ubicado.
    IndexError si la posición del barco se sale de los límites del tablero.
    ValueError si el barco se está posicionando sobre otro barco.
    """
    def ubicar(self, barco: Barco):
        if not barco or barco.getX() is None or barco.getY() is None:
            raise BaseException("El barco no se ha inicializado o ubicado")

        if barco.getOrientation() == Barco.HORIZONTAL:
            if barco.getX() > self._size - barco.getSize() or barco.getX() < 0 or barco.getY() >= self._size or barco.getY() < 0:
                raise IndexError("El barco se está posicionando fuera del tablero")

            for x in range(barco.getX(), barco.getX() + barco.getSize()):
                if self._celdas[barco.getY()][x].getBarco():
                    raise ValueError("El lugar está abarcado por otro barco")

            for x in range(barco.getX(), barco.getX() + barco.getSize()):
                self._celdas[barco.getY()][x].setBarco(barco)

        if barco.getOrientation() == Barco.VERTICAL:
            if barco.getX() >= self._size or barco.getX() < 0 or barco.getY() > self._size - barco.getSize() or barco.getY() < 0:
                raise IndexError("El barco se está posicionando fuera del tablero")

            for y in range(barco.getY(), barco.getY() + barco.getSize()):
                if self._celdas[y][barco.getX()].getBarco():
                    raise ValueError("El lugar está abarcado por otro barco")

            for y in range(barco.getY(), barco.getY() + barco.getSize()):
                self._celdas[y][barco.getX()].setBarco(barco)

    """
    Recibe un ataque en la posición especificada por los parámetros x, y.
    Arroja distintos errores si no se puede efectuar el ataque:

    IndexError -- Se está atacando una posición fuera de los límites del tablero.
    ValueError -- Se está atacando una celda que ya se atacó anteriormente.

    Retorna el resultado que tuvo el ataque.
    """
    def atacar(self, x: int, y: int) -> ResultadoAtaque:
        if x >= self._size or x < 0 or x >= self._size or y < 0:
            raise IndexError("Ataque fuera del tablero")

        celda = self._celdas[y][x]
        
        if celda.getHit():
            raise ValueError(f"Ya se ha atacado la celda ({x},{y})")

        celda.setHit()
        barco = celda.getBarco()

        if not barco:
            return ResultadoAtaque.FALLO

        barco.hit(max(x - barco.getX(), y - barco.getY()))

        if barco.destruido():
            return ResultadoAtaque.DESTRUIDO
        
        return ResultadoAtaque.IMPACTO

    def print(self) -> None:
        for row in self.toString():
            print(row)

    def toString(self) -> Generator[str, None, None]:
        yield "-".join(["+" for i in range(self._size + 1)])
        
        for i in range(self._size):
            row = "|"

            for j in range(self._size):
                cell = self._celdas[i][j]
                content = " "

                if not self._hidden:
                    if cell.getBarco():
                        content = "+"

                if cell.getHit():
                    if cell.getBarco():
                        content = "O"
                    else:
                        content = "X"

                row += f"{content}|"

            yield row
            yield "-".join(["+" for i in range(self._size + 1)])