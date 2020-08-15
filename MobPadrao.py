from time import time

from Entity import Entity
from random import random

class MobPadrao(Entity):
    def __init__(self, key, coordinates, dimensions, speed, acceleration, IMG_ASSETS):
        super().__init__(key, coordinates, dimensions, IMG_ASSETS)
        self.health = 1

        self._speed = speed  # in heights per second
        self.speed = speed * self.img.get_height()

        self._acceleration = acceleration  # in heights per second squared
        self.acceleration = acceleration * self.img.get_height()

        self.cooldown = .1
        self.timer = self.cooldown + 1

    def resize(self, window):
        super().resize(window)
        self.speed = self._speed * self.img.get_height()
        self.acceleration = self._acceleration * self.img.get_height()

    def fall(self, dt):
        self.speed += self.acceleration * dt
        self.coordinates[1] = round(self.coordinates[1] + self.speed * dt)

    def hit(self, dmg):
        self.health -= dmg

    def shoot(self, bullets, IMG_ASSETS, game_screen):
        bullet_speed = 5
        bullet = 'red bullet'
        now = time()
        r = random()
        print(r)
        if now - self.timer > self.cooldown and random() > .5:
            bullets.fire(bullet, [self.x + round(self.width / 2), self.y], self._dimensions,
                             IMG_ASSETS, bullet_speed, game_screen)
            self.timer = time()
