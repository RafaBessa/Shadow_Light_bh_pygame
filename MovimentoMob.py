from __future__ import annotations
from abc import ABC, abstractmethod


class AbstractMoviment(ABC):
    @abstractmethod
    def move(self, dt) -> None:
        pass


class Mov_LinearFall(AbstractMoviment):
    def move(self, coordinates, speed, acceleration, dt):
        speed += acceleration * dt
        coordinates[1] = round(coordinates[1] + speed * dt)
        return coordinates, speed, acceleration
        