import pygame
from Entity import Entity


class Bullets:
    def __init__(self, bullet_list, IMG_ASSETS):
        self.bullets = bullet_list

    def fire(self, key, coordinates, dimensions, IMG_ASSETS, speed):
        self.bullets.append(Bullet(key, coordinates, dimensions, IMG_ASSETS, speed))

    def move(self, dt):
        for i in self.bullets:
            i.move(dt)

    def resize(self, window):
        for i in self.bullets:
            i.resize(window)

    def draw(self, window):
        for i in self.bullets:
            i.draw(window)

    def hit(self, objs):
        for bullet in self.bullets:
            for obj in objs:
                if collide(bullet, obj):
                    obj.hit(bullet.dmg)


class Bullet(Entity):
    def __init__(self, key, coordinates, dimensions, IMG_ASSETS, speed):
        super().__init__(key, coordinates, dimensions, IMG_ASSETS)
        self.dmg = 1
        self._speed = speed
        self.speed = speed * self.img.get_width()

    def move(self, dt):
        self.coordinates[1] = round(self.coordinates[1] + self.speed * dt)

    def resize(self, window):
        super().resize(window)
        self.speed = self._speed * self.img.get_height()


def collide(obj1, obj2):
    return obj1.mask.overlap(obj2.mask, (obj2.x - obj1.x, obj2.y - obj1.y)) is not None
