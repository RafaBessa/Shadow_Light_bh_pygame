from Entity import Entity
import pygame
from time import time
import PlayerShoot as PS
import math
from ColorEnum import ColorEnum
from time import time


class Player(Entity):
    _ShootType = [PS.Shoot_Basic(), PS.Shoot_Double(), PS.Shoot_Triple()]

    class Healthbar(Entity):
        def __init__(self, dimensions, IMG_ASSETS, max_health):
            self.max_health = max_health
            selfh = IMG_ASSETS['healthbar'].get_height()
            super().__init__("healthbar", [0, dimensions[1] - selfh], dimensions, IMG_ASSETS)

        def hit(self, dmg):
            self.coordinates[0] -= round(self.width * dmg / self.max_health)

    def __init__(self, key, coordinates, dimensions, speed, IMG_ASSETS, bullet_key, bullet_speed, shotStrategy, fire_pattern):
        super().__init__(key, coordinates, dimensions, IMG_ASSETS)

        self.health = 10
        self.healthbar = self.Healthbar(dimensions, IMG_ASSETS, self.health)

        self._speed = speed  # in widths per second
        self.speed = speed * self.img.get_width()

        self.bullet_type = [bullet_key]
        self.bullet_speed = [bullet_speed]
        self.fire_pattern = fire_pattern

        self.cooldown = .1
        self.timer = self.cooldown + 1
        self.shootStrategy = shotStrategy
        self.score = 0
        self.killStreak = 0
        self.score_time = 0
        self.color = ColorEnum.Light
        self.colorDelay = 0

    def ChangeColor(self):
        if (time() - self.colorDelay) < 0.15:
            return
        self.colorDelay = time()
        if self.color == ColorEnum.Light:
            self.color = ColorEnum.Shadow
        else:
            self.color = ColorEnum.Light

    def draw(self, window):

        super().draw(window)

        pygame.font.init()
        font = pygame.font.SysFont("Comic Sans", 30)
        lost_font_rgb = (231, 88, 152)
        score_label = font.render("Score " + str(self.score), 1, lost_font_rgb)
        streak_label = font.render("Kill Streak " + str(self.killStreak), 1, lost_font_rgb)

        window._screen.blit(score_label, ((window.width - score_label.get_width() - 20), 5))
        window._screen.blit(streak_label, ((window.width - score_label.get_width() - 40 - streak_label.get_width()), 5))

        self.healthbar.draw(window)

    def hit(self, dmg):
        self.health -= dmg
        self.healthbar.hit(dmg)
        self.killStreak = 0

    def resize(self, window):
        super().resize(window)
        self.healthbar.resize(window)
        self.speed = self._speed * self.img.get_width()

    def move(self, key, window, dt, high_precision):
        u = (key[pygame.K_d] - key[pygame.K_a])
        v = (key[pygame.K_s] - key[pygame.K_w])
        modulus = (u ** 2 + v ** 2) ** .5

        # Checks for simultaneous WS or AD presses
        if modulus > 0:
            # making linear velocity equal to player velocity
            modulus = self.speed * dt / modulus
            if high_precision:
                modulus = 0.6 * modulus

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
                if self.coordinates[1] + v < self.healthbar.y - self.height:
                    # Moving
                    self.coordinates[1] += v
                else:
                    # Hugging lower border
                    self.coordinates[1] = self.healthbar.y - self.height
            else:
                # Hugging upper border
                self.coordinates[1] = 0

    @property
    def shoot_strg(self) -> PS.AbstractShoot:
        return self.shootStrategy

    @shoot_strg.setter
    def shoot_strg(self, atirar: PS.AbstractShoot) -> None:
        self.shootStrategy = self.shoot_met

    def shoot(self, bullets, IMG_ASSETS, game_screen, high_precision):
        # self.coordinates, self.speed, self.acceleration = self.mover_strg.move(self.coordinates, self.speed, self.acceleration, self._startcoordinate, dt)
        now = time()
        if now - self.timer > self.cooldown:
            self.shootStrategy.Shoot(bullets, IMG_ASSETS, game_screen, self.color,
                                     self.x, self.y, self.width, self.bullet_speed, self._dimensions, high_precision, self.fire_pattern)

            self.timer = time()

    def scoreUpdate(self, DeathCount, PassingCount):
        now = time()
        if now - self.score_time > 5:
            self.killStreak = 0
        self.score_time = now
        self.score += DeathCount
        self.killStreak += DeathCount
        _streakValue = 10
        if PassingCount > 0:
            self.killStreak = 0

        upgradetype = math.floor(self.killStreak / _streakValue)
        if upgradetype >= len(self._ShootType):
            upgradetype = len(self._ShootType) - 1

        self.shootStrategy = self._ShootType[upgradetype]
