from __future__ import annotations
from multiprocessing.sharedctypes import Value
from random import randint
from typing import List, Set
from logica.tablero import Celda, ResultadoAtaque, Tablero
from logica.barco import Barco

"""
Clase base para los jugadores:

Atributos:
tablero -- El tablero que pertenece al jugador
barcos -- Lista que contiene todos los barcos del jugador
"""
class JugadorBase:
    # 
    _tablero: Tablero
    _barcos: List[Barco]

    def __init__(self, tablero: Tablero, barcos: List[Barco]) -> None:
        self._tablero = tablero
        self._barcos = barcos

    """
    Getters
    """
    def getTablero(self) -> Tablero:
        return self._tablero

    def getBarcos(self) -> List[Barco]:
        return self._barcos

    """
    Retorna verdadero si todos los barcos del jugador han sido destruidos
    """
    def perdio(self) -> bool:
        for barco in self._barcos:
            if not barco.destruido():
                return False

        return True

    """
    Ubica a los barcos del jugador en el tablero
    """
    def ubicar(self):
        pass

    """
    Ataca al jugador que se pase como parámetro
    """
    def atacar(self, oponente: JugadorBase) -> ResultadoAtaque:
        pass


"""
Representa al jugador humano
"""
class Jugador(JugadorBase):
    def __init__(self, tablero: Tablero, barcos: List[Barco]) -> None:
        super().__init__(tablero, barcos)

    """
    Pregunta las posiciones de cada barco al jugador y los ubica en el tablero.
    Si se ingresa una posición inválida, vuelve a preguntar.
    """
    def ubicar(self):
        for barco in self._barcos:
            print(f"Posicionando barco {barco.getNombre()}:")
            sw = True

            while sw:
                x = int(input("x: "))
                y = int(input("y: "))
                orientacion = int(input("orientacion: "))
                
                try:
                    barco.ubicar(x, y, orientacion)
                    self._tablero.ubicar(barco)
                    sw = False
                except (IndexError, ValueError) as e:
                    print(e)

            self._tablero.print()


    """
    Pregunta por una posición en la cual atacar al enemigo.
    Si se ingresa una posición inválida, vuelve a preguntar.
    """
    def atacar(self, oponente: JugadorBase) -> ResultadoAtaque:
        while True:
            x = int(input("x: "))
            y = int(input("y: "))
            
            try:
                return oponente.getTablero().atacar(x, y)
            except (ValueError, IndexError) as e:
                print(e)


"""
Representa a la computadora.

Atributos:
memoria -- Almacena las celdas que ya se han atacado previamente.
"""
class Oponente(JugadorBase):
    _memoria: Set[Celda]

    def __init__(self, tablero: Tablero, barcos: List[Barco]) -> None:
        super().__init__(tablero, barcos)
        self._memoria = set()

    """
    Genera una orientación y posición aleatoria para el barco.
    Si se genera una posición inválida, vuelve a generar una.
    """
    def ubicar(self):
        for barco in self._barcos:
            orientacion = randint(1, 2)
            x = 0
            y = 0

            while True:
                try:
                    if orientacion == Barco.VERTICAL:
                        x = randint(0, self._tablero.getSize() - 1)
                        y = randint(0, self._tablero.getSize() - barco.getSize() - 1)

                    if orientacion == Barco.HORIZONTAL:
                        x = randint(0, self._tablero.getSize() - barco.getSize() - 1)
                        y = randint(0, self._tablero.getSize() - 1)
                    
                    barco.ubicar(x, y, orientacion)
                    self._tablero.ubicar(barco)

                    break
                except ValueError as e:
                    continue

    """
    Ataca a una posición aleatoria del campo del oponente procurando que no se ataque una misma posición más de una vez
    """
    def atacar(self, oponente: JugadorBase) -> ResultadoAtaque:
        sw = True
        x: int
        y: int

        while sw:
            x = randint(0, self._tablero.getSize() - 1)
            y = randint(0, self._tablero.getSize() - 1)
            cell = self._tablero.getCells()[y][x]

            if cell not in self._memoria:
                self._memoria.add(cell)
                sw = False
        
        return oponente.getTablero().atacar(x, y)
