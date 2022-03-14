from __future__ import annotations
from typing import List, Tuple

"""
Clase que representa las fichas que cada jugador tendrá disponible

Atributos:
name -- Nombre del barco
size -- Longitud que abarca el barco en celdas
pos -- Posición del barco. Es una tupla con la forma (x, y)
hits -- Una lista de booleanos con el mismo tamaño del barco que determina si una celda abarcada por el barco ha sido atacada.
Si todos los elementos de esta lista son verdaderos, el barco ha sido destruido.
orientation -- Orientación del barco 1: Vertical, 2: Horizontal
"""
class Barco():
    """Atributos estáticos, constantes que representan las orientaciones del barco"""
    VERTICAL = 1
    HORIZONTAL = 2

    _name: str
    _size: int
    _pos: Tuple[int, int]
    _hits: List[bool]
    _orientation: int

    def __init__(self, name: str, size: int):
        self._name = name
        self._size = size
        self._hits = [False for i in range(size)]

    """Getters"""
    def getNombre(self) -> str:
        return self._name

    def getSize(self) -> int:
        return self._size

    def getX(self) -> int:
        return self._pos[0]

    def getY(self) -> int:
        return self._pos[1]
    
    def getPos(self) -> Tuple[int, int]:
        return self._pos

    def getHits(self) -> List[bool]:
        return self._hits

    def getOrientation(self) -> int:
        return self._orientation

    """Impacta al barco en la posición denominada por el parámetro index"""
    def hit(self, index: int):
        self._hits[index] = True

    """Retorna verdadero no le quedan más puntos de vida al barco"""
    def destruido(self) -> bool:
        for hit in self._hits:
            if not hit:
                return False
        
        return True

    """Se le asigna la posición y orientación al barco"""
    def ubicar(self, x: int, y: int, orientacion: int):
        self._pos = (x, y)
        self._orientation = orientacion

    """Fabrica que genera un tipo de barco en específico dependiendo del nombre"""
    def getInstance(name: str) -> Barco:
        if name == "Submarino":
            return Submarino()
        
        if name == "Destructor":
            return Destructor()
        
        if name == "Crucero":
            return Crucero()
        
        if name == "Portaaviones":
            return Portaaviones()

        return None


"""Tipos de barco específicos"""
class Submarino(Barco):
    def __init__(self):
        super().__init__("Submarino", 1)


class Destructor(Barco):
    def __init__(self):
        super().__init__("Destructor", 2)


class Crucero(Barco):
    def __init__(self):
        super().__init__("Crucero", 3)


class Portaaviones(Barco):
    def __init__(self):
        super().__init__("Portaaviones", 4)