import Entity
import MovimentoMob as mm

class MobPadrao(Entity.Entity):
    def __init__(self, key, coordinates, dimensions, speed, acceleration, IMG_ASSETS, movStategy):
        super().__init__(key, coordinates, dimensions, IMG_ASSETS)
        self.health = 1

        self._speed = speed  # in heights per second
        self.speed = speed * self.img.get_height() #px/s

        self._acceleration = acceleration  # in heights per second squared
        self.acceleration = acceleration * self.img.get_height()
        self._movStrategy = movStategy
        self._startcoordinate = coordinates

    def resize(self, window):
        super().resize(window)
        self.speed = self._speed * self.img.get_height()
        self.acceleration = self._acceleration * self.img.get_height()

    @property
    def mover_strg(self) -> mm.AbstractMoviment:
        return self._movStrategy

    @mover_strg.setter
    def mover_strg(self, mover: mm.AbstractMoviment) -> None:
        self._movStrategy = fall

    def movimentar(self, dt):
        self.coordinates, self.speed, self.acceleration = self.mover_strg.move(self.coordinates, self.speed, self.acceleration, self._startcoordinate, dt)
   

    def hit(self, dmg):
        self.health -= dmg
