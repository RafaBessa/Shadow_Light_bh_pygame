from __future__ import annotations
from abc import ABC, abstractmethod


class AbstractShoot(ABC):
    @abstractmethod
    def Shoot(self, bullets, IMG_ASSETS, game_screen, bullet_type) -> None:
        pass


class Shoot_Basic(AbstractShoot):
    def Shoot(self,  bullets, IMG_ASSETS, game_screen, bullet_type, x, y, width, bullet_speed, dimensions):
        bullet = str(bullet_type)
        bullets.fire(bullet, [x + round(width / 2), y], dimensions,
                        IMG_ASSETS, bullet_speed[0], game_screen, bullet_type)


class Shoot_Double(AbstractShoot):
    def Shoot(self,  bullets, IMG_ASSETS, game_screen, bullet_type, x, y, width, bullet_speed, dimensions):
        bullet = str(bullet_type)
        bullets.fire(bullet, [x + round(width * 0.1), y], dimensions,
                        IMG_ASSETS, bullet_speed[0], game_screen, bullet_type)

        bullets.fire(bullet, [x + width - round(width * 0.3), y], dimensions,
                        IMG_ASSETS, bullet_speed[0], game_screen, bullet_type)
