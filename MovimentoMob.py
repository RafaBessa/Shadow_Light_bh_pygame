from __future__ import annotations
from abc import ABC, abstractmethod


class AbstractMoviment(ABC):
    @abstractmethod
    def move(self, dt) -> None:
        pass


class Mov_LinearFall(AbstractMoviment):
    def move(self, coordinates, speed, acceleration, lastcoordinate,screen,direction, dt ):
        speed += acceleration * dt
        coordinates[1] = round(coordinates[1] + speed * dt)
        return coordinates, speed, acceleration, direction
        

class Mov_ZigZag(AbstractMoviment):
    
    def move(self, coordinates, speed, acceleration, startcoordinate,screen,direction, dt ):
        ZigZageamento = 100 #variacao max da nave
        coordinates[1] = round(coordinates[1] + speed * dt)


        if (startcoordinate[0] + ZigZageamento  >= coordinates[0] ) and (direction): #se ele tava na esquerda vai pra direita 
            coordinates[0] = round(coordinates[0] + speed * dt)

        elif (startcoordinate[0] - ZigZageamento  <= coordinates[0] ) and (not direction) :
            coordinates[0] = round(coordinates[0] - speed * dt)
        
        else:
            direction = not direction

        if(coordinates[0] < 0):
            coordinates[0] = 0
        return coordinates, speed, acceleration, direction


class Mov_HorizontalBossLeft(AbstractMoviment):
    
    def move(self, coordinates, speed, acceleration, lastcoordinate,screen, direction, dt):
        speed += acceleration * dt
        Maxx, Maxy = screen
        if not direction:
            if(coordinates[0] + speed ) >= Maxx:
                direction = True
            else:
                coordinates[0] = round(coordinates[0] + speed)
            
        else:
            if(coordinates[0] - speed ) <= 0:
                direction = False
            else:
                coordinates[0] = round(coordinates[0] - speed)

        return coordinates, speed, acceleration, direction

class Mov_HorizontalBossRight(AbstractMoviment):
    
    def move(self, coordinates, speed, acceleration, lastcoordinate, screen,direction, dt):
        
        speed += acceleration * dt
        Maxx, Maxy = screen
        if direction:
            if(coordinates[0] + speed ) >= Maxx:
                direction = False
            else:
                coordinates[0] = round(coordinates[0] + speed)
            
        else:
            if(coordinates[0] - speed ) <= 0:
                direction = True
            else:
                coordinates[0] = round(coordinates[0] - speed)
            

        return coordinates, speed, acceleration, direction


class Mov_HorizontalAglom(AbstractMoviment):

    def move(self, coordinates, speed, acceleration, startcoordinate, screen, direction, dt):
        ZigZageamento = 100  # variacao max da nave

        if (startcoordinate[0] + ZigZageamento >= coordinates[0]) and (
        direction):  # se ele tava na esquerda vai pra direita
            coordinates[0] = round(coordinates[0] + speed * dt)

        elif (startcoordinate[0] - ZigZageamento <= coordinates[0]) and (not direction):
            coordinates[0] = round(coordinates[0] - speed * dt)

        else:
            direction = not direction

        if (coordinates[0] < 0):
            coordinates[0] = 0
        return coordinates, speed, acceleration, direction
