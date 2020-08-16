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

    class Hitbox(Entity):
        def __init__(self, coordinates, dimensions, IMG_ASSETS):
            self.key_light = "hit light"
            self.key_dark = "hit dark"
            self.color = ColorEnum.Light
            super().__init__(self.key_light, coordinates, dimensions, IMG_ASSETS)

        def ChangeColor(self):
            if self.color == ColorEnum.Light:
                self.img_key = self.key_dark
                self.color = ColorEnum.Shadow
            else:
                self.img_key = self.key_light
                self.color = ColorEnum.Light

        def draw_at(self, window, coordinates):
            self.coordinates = coordinates
            self.resize(window)
            super().draw(window)



    def __init__(self, coordinates, dimensions, speed, IMG_ASSETS, bullet_key, bullet_speed):
        self.key_light = "ship light"
        self.key_dark = "ship dark"

        super().__init__(self.key_light, coordinates, dimensions, IMG_ASSETS)

        self.health = 10
        self.healthbar = self.Healthbar(dimensions, IMG_ASSETS, self.health)

        self._hitbox = self.Hitbox(coordinates, dimensions, IMG_ASSETS)

        self.high_precision = False

        self._speed = speed  # in widths per second
        self.speed = speed * self.img.get_width()
        self.bullet_type = [bullet_key]
        self._startbullet_speed = [bullet_speed]
        self.bullet_speed = [bullet_speed]

        self.cooldown = .1
        self._startcooldown = .1
        self.timer = self.cooldown + 1
        self.score = 0
        self.killStreak = 0
        self.score_time = 0
        self.color = ColorEnum.Light
        self.colorDelay = 0

    def ChangeColor(self, window):
        if (time() - self.colorDelay) < 0.15:
            return
        self.colorDelay = time()
        self._hitbox.ChangeColor()
        if self.color == ColorEnum.Light:
            self.color = ColorEnum.Shadow
            self.img_key = self.key_dark
        else:
            self.color = ColorEnum.Light
            self.img_key = self.key_light
        self.resize(window)

    def draw(self, window):
        super().draw(window)
        if self.high_precision:
            self._hitbox.draw_at(window, self.coordinates)
        pygame.font.init()
        font = pygame.font.SysFont("Comic Sans", 30)
        lost_font_rgb = (231, 88, 152)
        score_label = font.render("Score " + str(self.score), 1, lost_font_rgb)
        streak_label = font.render("Kill Streak " + str(self.killStreak), 1, lost_font_rgb)

        window._screen.blit(score_label, ((window.width - score_label.get_width() - 20), 5))
        window._screen.blit(streak_label, ((window.width - score_label.get_width() - 40 - streak_label.get_width()), 5))

        self.healthbar.draw(window)

    def hit(self, dmg, bullet_type):
        if not (bullet_type == self.color):
            self.health -= dmg
            self.healthbar.hit(dmg)
            self.killStreak = 0
            self.cooldown = self._startcooldown
            self.speed = self._speed * self.img.get_width()
            self.bullet_speed[0] = self._startbullet_speed[0]

    def resize(self, window):
        super().resize(window)
        self.healthbar.resize(window)
        self._hitbox.resize(window)
        self.speed = self._speed * self.img.get_width()

    def move(self, key, window, dt):
        u = (key[pygame.K_d] - key[pygame.K_a])
        v = (key[pygame.K_s] - key[pygame.K_w])
        modulus = (u ** 2 + v ** 2) ** .5

        # Checks for simultaneous WS or AD presses
        if modulus > 0:
            # making linear velocity equal to player velocity
            modulus = self.speed * dt / modulus
            if self.high_precision:
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
    def hitbox(self):
        if self.high_precision:
            return self._hitbox
        else:
            return self

    @property
    def shoot_strg(self) -> PS.AbstractShoot:
        return self.shootStrategy

    @shoot_strg.setter
    def shoot_strg(self, atirar: PS.AbstractShoot) -> None:
        self.shootStrategy = self.shoot_met

    def shoot(self, bullets, IMG_ASSETS, game_screen):
        # self.coordinates, self.speed, self.acceleration = self.mover_strg.move(self.coordinates, self.speed, self.acceleration, self._startcoordinate, dt)
        now = time()
        if now - self.timer > self.cooldown:
            self.shootStrategy.Shoot(bullets, IMG_ASSETS, game_screen, self.color,
                                     self.x, self.y, self.width, self.bullet_speed, self._dimensions, self.high_precision)

            self.timer = time()

    def scoreUpdate(self, DeathCount, PassingCount):
        print(str(self.speed))
        now = time()
        if now - self.score_time > 5:
            self.killStreak = 0
        self.score_time = now
        self.score += DeathCount
        self.killStreak += DeathCount
        _streakValue = 10
        # if PassingCount > 0:
        #     self.killStreak = 0
        if DeathCount>=1:
       #     print(str(self.bullet_speed) + " , " +  str(self.cooldown))
            self.bullet_speed[0] *= 1.10
            self.cooldown *= 1.15
            self.speed *= 1.06
            #print(str(self.speed))
        upgradetype = math.floor(self.killStreak / _streakValue)
        if upgradetype >= len(self._ShootType):
            upgradetype = len(self._ShootType) - 1

        self.shootStrategy = self._ShootType[upgradetype]
