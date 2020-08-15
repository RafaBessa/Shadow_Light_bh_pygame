import Entity


class Droplet(Entity.Entity):
    def __init__(self, key, coordinates, dimensions, speed, acceleration, IMG_ASSETS):
        super().__init__(key, coordinates, dimensions, IMG_ASSETS)

        self._speed = speed  # in heights per second
        self.speed = speed * self.img.get_height()

        self._acceleration = acceleration  # in heights per second squared
        self.acceleration = acceleration * self.img.get_height()

    def resize(self, window):
        super().resize(window)
        self.speed = self._speed * self.img.get_height()
        self.acceleration = self._acceleration * self.img.get_height()

    def fall(self, dt):
        self.speed += self.acceleration * dt
        self.coordinates = (self.coordinates[0], round(self.coordinates[1] + self.speed * dt))
