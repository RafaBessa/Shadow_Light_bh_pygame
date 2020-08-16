from __future__ import annotations
from abc import ABC, abstractmethod


class AbstractMoviment(ABC):
    @abstractmethod
    def move(self, dt) -> None:
        pass


class Mov_LinearFall(AbstractMoviment):
    def move(self, coordinates, speed, acceleration, lastcoordinate, dt):
        speed += acceleration * dt
        coordinates[1] = round(coordinates[1] + speed * dt)
        return coordinates, speed, acceleration
        

class Mov_ZigZag(AbstractMoviment):
    direct = True
    def move(self, coordinates, speed, acceleration, startcoordinate, dt):
        ZigZageamento = 100 #variacao max da nave
        coordinates[1] = round(coordinates[1] + speed * dt)


        if (startcoordinate[0] + ZigZageamento  >= coordinates[0] ) and (self.direct): #se ele tava na esquerda vai pra direita 
            coordinates[0] = round(coordinates[0] + speed * dt)

        elif (startcoordinate[0] - ZigZageamento  <= coordinates[0] ) and (not self.direct) :
            coordinates[0] = round(coordinates[0] - speed * dt)
        
        else:
            self.direct = not self.direct

        if(coordinates[0] < 0):
            coordinates[0] = 0
        return coordinates, speed, acceleration
