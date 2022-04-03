from __future__ import annotations
from typing import Dict, Generator
from typing import List, Set, Tuple
from random import randint, random
import pygame
import pygame_gui

"""Lee el tamaño del tablero de juego y lo inicializa"""
size = 0

"""
El tablero de juego, en cada juego se tienen 2 instancias de estos. Una para cada jugador.

Atributos:
celdas -- Matriz cuadrada que contiene a todas las celdas que hacen parte del tablero con tamaño size x size
size -- Tamaño del tablero
hidden -- Booleano que si está activado no permite que se vean los barcos en el tablero.
Por defecto para el jugador es Falso y para la computadora es Verdadero
"""
class Tablero:
    SPRITE_NORMAL = pygame.image.load("res/water.png")
    SPRITE_BARCO = pygame.image.load("res/ship.png")
    CELL_SIZE = 32

    _celdas: List[List[Barco]]
    _barcos: List[Barco]
    _colores: Dict[Barco, pygame.Color]
    _size: int

    def __init__(self, size: int) -> None:
        self._size = size
        self._celdas = [[None for j in range(size)] for i in range(size)]
        self._barcos = []
        self._colores = {}

    """Getters"""
    def getSize(self) -> int:
        return self._size

    def getCeldas(self) -> List[List[Barco]]:
        return self._celdas
    
    def getPixelSize(self) -> int:
        return self._size * Tablero.CELL_SIZE

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

    def print(self) -> pygame.Surface:
        size = len(self._celdas) * Tablero.CELL_SIZE
        tablero = pygame.Surface((size, size))
        tablero.fill(pygame.Color(51, 204, 51))
        baseRect: pygame.Rect = Tablero.SPRITE_NORMAL.get_rect()

        for i in range(self._size):
            for j in range(self._size):
                rect = baseRect.move(j * Tablero.CELL_SIZE, i * Tablero.CELL_SIZE)
                barco = self._celdas[i][j]

                if barco:
                    color = None

                    if barco in self._colores:
                        color = self._colores[barco]
                    else:
                        color = pygame.Color(randint(0, 200), randint(0, 150), randint(0, 150))
                        self._colores[barco] = color
                    
                    tablero.blit(Tablero.SPRITE_BARCO, rect)
                    texto = pygame.font.SysFont(None, 24)
                    img = texto.render(str(barco.getId()), True, color)
                    tablero.blit(img, rect.move(5, 5))
                else:
                    tablero.blit(Tablero.SPRITE_NORMAL, rect)

        return tablero
                
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
    barcosGenerados = ["Tamaño tablero", "Submarino", "Destructor", "Crucero", "Portaaviones"]

    pygame.init()
    displaySize = (700, 500)
    display = pygame.display.set_mode(displaySize, pygame.RESIZABLE)
    ejecutandose = True
    fps = pygame.time.Clock()
    manager = pygame_gui.UIManager(displaySize)
    elemSize = pygame.Rect(0, 0, 200, 35)

    campos = [
        (
            pygame_gui.elements.UITextBox(barcosGenerados[i], relative_rect=elemSize.move(50, 75 * i + 20), manager=manager),
            pygame_gui.elements.UITextEntryLine(elemSize.move(50, 75 * i + 50), manager=manager)
        ) for i in range(len(barcosGenerados))
    ]

    for campo in campos:
        campo[1].set_allowed_characters("numbers")

    confirmar = pygame_gui.elements.UIButton(relative_rect=elemSize.move(50, 410).inflate(0, 20), text="Confirmar", manager=manager)
    texto = ""

    while ejecutandose:
        delta = fps.tick(30) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutandose = False

            if event.type == pygame.KEYDOWN:
                for campo in campos:
                    if campo[1].is_focused:
                        if event.key == pygame.K_BACKSPACE:
                            campo[1].set_text(campo[1].get_text()[:-1])
                        else:
                            campo[1].set_text(campo[1].get_text() + event.unicode)

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                try:
                    if event.ui_element == confirmar:
                        Barco.secuencia_id = 0

                        size = campos[0][1].get_text()
                        submarinos = campos[1][1].get_text()
                        destructores = campos[2][1].get_text()
                        cruceros = campos[3][1].get_text()
                        portaaviones = campos[4][1].get_text()

                        size = int(size) if size != "" else 0
                        submarinos = int(submarinos) if submarinos != "" else 0
                        destructores = int(destructores) if destructores != "" else 0
                        cruceros = int(cruceros) if cruceros != "" else 0
                        portaaviones = int(portaaviones) if portaaviones != "" else 0

                        tablero = Tablero(size)
                        pixelSize = tablero.getPixelSize()

                        if pixelSize > 400:
                            displaySize = (300 + pixelSize, 50 + pixelSize)
                        else:
                            displaySize = (700, 500)

                        display = pygame.display.set_mode(displaySize, pygame.RESIZABLE)

                        """Lee el número de los distintos barcos que tendrá el juego"""
                        numBarcos: Dict[str, int] = {
                            "Submarino": int(submarinos),
                            "Destructor": int(destructores),
                            "Crucero": int(cruceros),
                            "Portaaviones": int(portaaviones)
                        }

                        """Genera los barcos para un jugador dependiendo del anterior diccionario"""
                        barcosGenerados = [Barco.generar(barco) for barco in numBarcos for i in range(numBarcos[barco])]
                        
                        for barco in barcosGenerados:
                            if barco.getSize() > size:
                                raise ValueError(f"El barco {barco.getNombre()} {barco.getId()} tiene un tamaño mayor al del tablero, no se puede posicionar.")

                            if not barco.ubicar():
                                raise ValueError(f"No se pudo ubicar el barco {barco.getNombre()} {barco.getId()} en el tablero. No hay espacio disponible")
                except ValueError as e:
                    texto = str(e)
                except:
                    texto = "No se pudieron ubicar los barcos en el tablero"
                
        try:
            manager.process_events(event)
        except:
            pass

        manager.update(delta)

        imagenTablero = tablero.print()
        display.fill(pygame.Color(200, 200, 200))
        display.blit(imagenTablero, imagenTablero.get_rect().move(270, 20))

        font = pygame.font.SysFont(None, 24)
        img = font.render(texto, True, pygame.Color(255, 0, 0))
        display.blit(img, (20, 20))
        manager.draw_ui(display)
        pygame.display.flip()
        pygame.display.update()

    pygame.quit()