from Entity import Entity
import pygame
from time import time
import PlayerShoot as PS
from enum import Enum
import math
class Player(Entity):
    _ShootType = [PS.Shoot_Basic(), PS.Shoot_Double()]
    def __init__(self, key, coordinates, dimensions, speed, IMG_ASSETS, bullet_key, bullet_speed, shotStrategy):
        super().__init__(key, coordinates, dimensions, IMG_ASSETS)
        self._speed = speed  # in widths per second
        self.speed = speed * self.img.get_width()

        self.bullet_type = [bullet_key]
        self.bullet_speed = [bullet_speed]

        self.cooldown = .1
        self.timer = self.cooldown + 1
        self.shootStrategy = shotStrategy
        self.score = 0
        self.killStreak = 0
    def resize(self, window):
        super().resize(window)
        self.speed = self._speed * self.img.get_width()

    def walk(self, key, window, dt):
        u = (key[pygame.K_d] - key[pygame.K_a])
        v = (key[pygame.K_s] - key[pygame.K_w])
        modulus = (u ** 2 + v ** 2) ** .5

        # Checks for simultaneous WS or AD presses
        if modulus > 0:
            # making linear velocity equal to player velocity
            modulus = self.speed * dt / modulus
            u = round(u * modulus)
            v = round(v * modulus)
            # Checking left border
            if self.coordinates[0] + u > 0:
                # Checking right border
                if self.coordinates[0] + u < window.width - self.width:
                    # Moving
                    self.coordinates[0] += u
                else:
                    # Hugging right
                    self.coordinates[0] = window.width - self.width
            else:
                # Hugging left
                self.coordinates[0] = 0

            # Checking upper border
            if self.coordinates[1] + v > 0:
                # Checking lower border
                if self.coordinates[1] + v < window.height - self.height:
                    # Moving
                    self.coordinates[1] += v
                else:
                    # Hugging lower border
                    self.coordinates[1] = window.height - self.height
            else:
                # Hugging upper border
                self.coordinates[1] = 0


    @property
    def shoot_strg(self) -> PS.AbstractShoot:
        return self.shootStrategy

    @shoot_strg.setter
    def shoot_strg(self, atirar: PS.AbstractShoot) -> None:
        self.shootStrategy = self.shoot_met

    def shoot(self, bullets, IMG_ASSETS, game_screen):
        #self.coordinates, self.speed, self.acceleration = self.mover_strg.move(self.coordinates, self.speed, self.acceleration, self._startcoordinate, dt)
        now = time()
        if now - self.timer > self.cooldown:
            
            self.shootStrategy.Shoot(bullets, IMG_ASSETS, game_screen, self.bullet_type, 
            self.x, self.y, self.width, self.bullet_speed, self._dimensions)


            self.timer = time()




    def scoreUpdate(self, DeathCount, PassingCount):
        self.score += DeathCount
        self.killStreak += DeathCount
        _streakValue = 1
        if(PassingCount > 0):
            killStreak = 0
        
        upgradetype = math.floor(self.killStreak/_streakValue)
        if upgradetype >= len(self._ShootType):
            upgradetype = len(self._ShootType) - 1
        self.shootStrategy = self._ShootType[upgradetype] 


    
    def DrawScore(window):

        window.draw(self.img, self.coordinates)