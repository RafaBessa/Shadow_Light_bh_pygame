from time import time

from random import random
from copy import copy
from Entity import Entity
import MovimentoMob as mm
import pygame
import PlayerShoot as PS
class MobPadrao(Entity):
    def __init__(self, key, coordinates, dimensions, speed, acceleration, IMG_ASSETS, bulletType, movStategy, cooldown, life = 1, shootStrategy = PS.Shoot_Basic()):

        super().__init__(key, coordinates, dimensions, IMG_ASSETS)
        self.health = life
        self._starthealth = copy(life)
        self.bulletType = bulletType
        self._speed = speed  # in heights per second
        self.speed = speed * self.img.get_height() #px/s
        self._acceleration = acceleration  # in heights per second squared
        self.acceleration = acceleration * self.img.get_height()
        self._movStrategy = movStategy
        self._startcoordinate = coordinates
        self.cooldown = cooldown
        self.timer = self.cooldown + 1
        self.direction = True
        self.high_precision = False
        self.shootStrategy = shootStrategy
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
        self.coordinates, self.speed, self.acceleration, self.direction = self.mover_strg.move(self.coordinates, self.speed, self.acceleration, self._startcoordinate, self._dimensions, self.direction, dt)
                                                                                
    def hit(self, dmg, bulletType):
        
        if not (bulletType == self.bulletType):
            self.health -= dmg

    # def shoot(self, bullets, IMG_ASSETS, game_screen):
    #     bullet_speed = 4
    #     bullet = 'red bullet'
    #     now = time()
    #     r = random()
      
    #     if now - self.timer > self.cooldown and random() > .3:
    #         bullets.fire(bullet, [self.x + round(self.width / 2), self.y + round(0.8 * self.height)], self._dimensions,
    #                          IMG_ASSETS, (bullet_speed + round(0.1*self.speed)), game_screen, self.bulletType, mb.Mov_LinearFall())
    #         self.timer = time()



    @property
    def shoot_strg(self) -> PS.AbstractShoot:
        return self.shootStrategy

    @shoot_strg.setter
    def shoot_strg(self, atirar: PS.AbstractShoot) -> None:
        self.shootStrategy = self.shoot_met

    def shoot(self, bullets, IMG_ASSETS, game_screen):
        # self.coordinates, self.speed, self.acceleration = self.mover_strg.move(self.coordinates, self.speed, self.acceleration, self._startcoordinate, dt)
        bullet_speed = 4
        bullet = 'red bullet'
        now = time()
        r = random()
        args = {"calcTime": now - self.timer, "cd" : self.cooldown }
    
        if  random() > .3:
            didshoot = self.shootStrategy.Shoot(bullets, IMG_ASSETS, game_screen, self.bulletType,
                                    self.x , self.y + round(0.8 * self.height), self.width, (bullet_speed+ round(0.1*self.speed)), self._dimensions,
                                    self.high_precision, args = args)
            if didshoot:
                self.timer = time()




    def draw(self, window):
        
        # cimg = cimg.fill((0, 100, 200))
        window.draw(self.img, self.coordinates)
        if self._starthealth > 1:
            percent = self.health / self._starthealth
            pygame.draw.rect(window._screen, (255,0,0), (self.coordinates[0] + round(self.width/2), self.coordinates[1] - 10, 50, 5)) # NEW
            pygame.draw.rect(window._screen, (0,128,0), (self.coordinates[0] + round(self.width/2), self.coordinates[1] - 10, round(50 * percent) , 5)) # NEW