from time import time

from random import random
from copy import copy
import Entity
import MovimentoMob as mm
import MovimentoBala as mb

class MobPadrao(Entity.Entity):
    def __init__(self, key, coordinates, dimensions, speed, acceleration, IMG_ASSETS, bulletType, movStategy, cooldown, life = 1):

        super().__init__(key, coordinates, dimensions, IMG_ASSETS)
        self.health = life
        self.bulletType = bulletType
        self._speed = speed  # in heights per second
        self.speed = speed * self.img.get_height() #px/s
        self._acceleration = acceleration  # in heights per second squared
        self.acceleration = acceleration * self.img.get_height()
        self._movStrategy = movStategy
        self._startcoordinate = coordinates
        self.cooldown = cooldown
        self.timer = self.cooldown + 1

    def resize(self, window):
        super().resize(window)
        self.speed = self._speed * self.img.get_height()
        self.acceleration = self._acceleration * self.img.get_height()

    @property
    def mover_strg(self) -> mm.AbstractMoviment:
        return self._movStrategy

    @mover_strg.setter
    def mover_strg(self, mover: mm.AbstractMoviment) -> None:
        self._movStrategy = mover

    def movimentar(self, dt):
        self.coordinates, self.speed, self.acceleration = self.mover_strg.move(self.coordinates, self.speed, self.acceleration, self._startcoordinate, self._dimensions, dt)
                                                                                
    def hit(self, dmg, bulletType):
        
        if not (bulletType == self.bulletType):
            self.health -= dmg

    def shoot(self, bullets, IMG_ASSETS, game_screen):
        bullet_speed = 4
        bullet = 'red bullet'
        now = time()
        r = random()
      
        if now - self.timer > self.cooldown and random() > .3:
            bullets.fire(bullet, [self.x + round(self.width / 2), self.y + round(0.8 * self.height)], self._dimensions,
                             IMG_ASSETS, (bullet_speed + round(0.1*self.speed)), game_screen, self.bulletType, mb.Mov_LinearFall())
            self.timer = time()

    def draw(self, window):
        cimg = copy(self.img)
        # cimg = cimg.fill((0, 100, 200))
        window.draw(cimg, self.coordinates)
