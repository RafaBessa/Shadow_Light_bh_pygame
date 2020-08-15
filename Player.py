import Entity
import pygame
from time import time

class Player(Entity.Entity):

    def __init__(self, key, coordinates, dimensions, speed, IMG_ASSETS, bullet_key, bullet_speed):
        super().__init__(key, coordinates, dimensions, IMG_ASSETS)
        self._speed = speed  # in widths per second
        self.speed = speed*self.img.get_width()

        self.bullet_type = [bullet_key]
        self.bullet_speed = [bullet_speed]

        self.cooldown = .1
        self.timer = self.cooldown+1

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

    def shoot(self, bullets, IMG_ASSETS):
        now = time()
        if now - self.timer > self.cooldown:
            for i, bullet in enumerate(self.bullet_type):
                bullets.fire(self.bullet_type[i], [self.x + round(self.width/2), self.y], self._dimensions, IMG_ASSETS, self.bullet_speed[i])
            self.timer = time()
