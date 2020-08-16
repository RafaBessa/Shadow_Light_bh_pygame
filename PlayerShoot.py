from __future__ import annotations
from abc import ABC, abstractmethod
import MovimentoBala as mb

class AbstractShoot(ABC):
    @abstractmethod
    def Shoot(self, bullets, IMG_ASSETS, game_screen, bullet_type) -> None:
        pass


class Shoot_Basic(AbstractShoot):
    def Shoot(self,  bullets, IMG_ASSETS, game_screen, bullet_type, x, y, width, bullet_speed, dimensions, high_precision, fire_pattern):
        bullet = str(bullet_type)
        bullets.fire(bullet, [x + round(width / 2), y], dimensions,
                        IMG_ASSETS, bullet_speed[0], game_screen, bullet_type, fire_pattern)


class Shoot_Double(AbstractShoot):
    def Shoot(self,  bullets, IMG_ASSETS, game_screen, bullet_type, x, y, width, bullet_speed, dimensions, high_precision, fire_pattern):
        bullet = str(bullet_type)
        if high_precision:
            bullets.fire(bullet, [x + round(width * 0.4), y], dimensions,
                            IMG_ASSETS, bullet_speed[0], game_screen, bullet_type, fire_pattern)

            bullets.fire(bullet, [x + round(width * 0.6), y], dimensions,
                            IMG_ASSETS, bullet_speed[0], game_screen, bullet_type, fire_pattern)
        else:
            bullets.fire(bullet, [x + round(width * 0.1), y], dimensions,
                            IMG_ASSETS, bullet_speed[0], game_screen, bullet_type, fire_pattern)

            bullets.fire(bullet, [x + round(width * 0.7), y], dimensions,
                            IMG_ASSETS, bullet_speed[0], game_screen, bullet_type, fire_pattern)


class Shoot_Triple(AbstractShoot):
    center_shoot = Shoot_Basic.Shoot
    def Shoot(self,  bullets, IMG_ASSETS, game_screen, bullet_type, x, y, width, bullet_speed, dimensions, high_precision, fire_pattern):
        bullet = str(bullet_type)
        if high_precision:
            bullets.fire(bullet, [x + round(width * 0.4), y], dimensions,
                            IMG_ASSETS, bullet_speed[0], game_screen, bullet_type, mb.Mov_DiagLeft())

            bullets.fire(bullet, [x + round(width * 0.6), y], dimensions,
                            IMG_ASSETS, bullet_speed[0], game_screen, bullet_type, mb.Mov_DiagRight())
        else:
            bullets.fire(bullet, [x + round(width * 0.1), y], dimensions,
                            IMG_ASSETS, bullet_speed[0], game_screen, bullet_type, mb.Mov_DiagLeft())

            bullets.fire(bullet, [x + round(width * 0.7), y], dimensions,
                            IMG_ASSETS, bullet_speed[0], game_screen, bullet_type, mb.Mov_DiagRight())
        self.center_shoot(bullets, IMG_ASSETS, game_screen, bullet_type, x, y, width, bullet_speed, dimensions, high_precision, fire_pattern)
