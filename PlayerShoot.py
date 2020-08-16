from __future__ import annotations
from abc import ABC, abstractmethod
import MovimentoBala as mb



class AbstractShoot(ABC):
    @abstractmethod
    def Shoot(self, bullets, IMG_ASSETS, game_screen, bullet_type) -> None:
        pass


class Shoot_Basic(AbstractShoot):
    def Shoot(self,  bullets, IMG_ASSETS, game_screen, bullet_type, x, y, width, bullet_speed, dimensions, high_precision):
        bullet = str(bullet_type)
        
        bullets.fire(bullet, [x + round(width / 2), y], dimensions,
                        IMG_ASSETS, bullet_speed, game_screen, bullet_type, mb.Mov_LinearFall())


class Shoot_Double(AbstractShoot):
    def Shoot(self,  bullets, IMG_ASSETS, game_screen, bullet_type, x, y, width, bullet_speed, dimensions, high_precision):
        bullet = str(bullet_type)
        if high_precision:
            bullets.fire(bullet, [x + round(width * 0.4), y], dimensions,
                            IMG_ASSETS, bullet_speed, game_screen, bullet_type, mb.Mov_LinearFall())

            bullets.fire(bullet, [x + round(width * 0.6), y], dimensions,
                            IMG_ASSETS, bullet_speed, game_screen, bullet_type, mb.Mov_LinearFall())
        else:
            bullets.fire(bullet, [x + round(width * 0.1), y], dimensions,
                            IMG_ASSETS, bullet_speed, game_screen, bullet_type,  mb.Mov_LinearFall())

            bullets.fire(bullet, [x + round(width * 0.7), y], dimensions,
                            IMG_ASSETS, bullet_speed, game_screen, bullet_type,  mb.Mov_LinearFall())


class Shoot_Triple(AbstractShoot):
    center_shoot = Shoot_Basic.Shoot
    def Shoot(self,  bullets, IMG_ASSETS, game_screen, bullet_type, x, y, width, bullet_speed, dimensions, high_precision):
        bullet = str(bullet_type)
        if high_precision:
            bullets.fire(bullet, [x + round(width * 0.4), y], dimensions,
                            IMG_ASSETS, bullet_speed, game_screen, bullet_type, mb.Mov_DiagRight(.08))

            bullets.fire(bullet, [x + round(width * 0.6), y], dimensions,
                            IMG_ASSETS, bullet_speed, game_screen, bullet_type,  mb.Mov_DiagLeft(.08))
        else:
            bullets.fire(bullet, [x + round(width * 0.1), y], dimensions,
                            IMG_ASSETS, bullet_speed, game_screen, bullet_type,  mb.Mov_DiagLeft(.17))

            bullets.fire(bullet, [x + round(width * 0.7), y], dimensions,
                            IMG_ASSETS, bullet_speed, game_screen, bullet_type,  mb.Mov_DiagRight(.17))
        self.center_shoot(bullets, IMG_ASSETS, game_screen, bullet_type, x, y, width, bullet_speed, dimensions, high_precision)
