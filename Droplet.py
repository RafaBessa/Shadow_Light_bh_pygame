import Entity
class Droplet(Entity.Entity):
    def __init__(self, key, coordinates, dimensions, speed, acceleration):
        super().__init__(key, coordinates, dimensions)

        self._speed = speed  # in heights per second
        self.speed = speed*self.img.get_height()

        self._acceleration = acceleration  # in heights per second squared
        self.acceleration = acceleration*self.img.get_height()

    def resize(self, window):
        super().resize(window)
        self.speed = self._speed * self.img.get_height()
        self.acceleration = self._acceleration*self.img.get_height()

    def fall(self, dt):
        self.speed += self.acceleration*dt
        self.coordinates = (self.coordinates[0], self.coordinates[1]+self.speed*dt)


