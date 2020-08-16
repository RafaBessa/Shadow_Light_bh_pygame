from __future__ import annotations
from abc import ABC, abstractmethod


class AbstractMoviment(ABC):
    @abstractmethod
    def move(self, dt) -> None:
        pass


class Mov_LinearFall(AbstractMoviment):
    def move(self, coordinates, speed, lastcoordinate, dt):
        coordinates[1] = round(coordinates[1] + speed * dt)
        return coordinates, speed


class Mov_ZigZag(AbstractMoviment):
    direct = True

    def move(self, coordinates, speed, startcoordinate, dt):
        ZigZageamento = 100  # variacao max da nave
        coordinates[1] = round(coordinates[1] + speed * dt)

        if (startcoordinate[0] + ZigZageamento >= coordinates[0]) and (
        self.direct):  # se ele tava na esquerda vai pra direita
            coordinates[0] = round(coordinates[0] + speed * dt)

        elif (startcoordinate[0] - ZigZageamento <= coordinates[0]) and (not self.direct):
            coordinates[0] = round(coordinates[0] - speed * dt)

        else:
            self.direct = not self.direct

        return coordinates, speed

class Mov_DiagRight(AbstractMoviment):

    def move(self, coordinates, speed, startcoordinate, dt):
        ZigZageamento = 100  # variacao max da nave
        coordinates[1] = round(coordinates[1] + speed * dt)
        coordinates[0] = round(coordinates[0] + speed/2 * dt)

        return coordinates, speed

class Mov_DiagLeft(AbstractMoviment):

    def move(self, coordinates, speed, startcoordinate, dt):
        ZigZageamento = 100  # variacao max da nave
        coordinates[1] = round(coordinates[1] + speed * dt)
        coordinates[0] = round(coordinates[0] - speed/2 * dt)

        return coordinates, speed