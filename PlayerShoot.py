from __future__ import annotations
from abc import ABC, abstractmethod
import MovimentoBala as mb
import pygame
import ColorEnum

 
class AbstractShoot(ABC):
    def calcCd(self,args):
        return (args["calcTime"] > args["cd"])
    @abstractmethod
    def Shoot(self, bullets, IMG_ASSETS, game_screen, bullet_type) -> None:
        pass


class Shoot_Basic(AbstractShoot):
    def Shoot(self,  bullets, IMG_ASSETS, game_screen, bullet_type, x, y, width, bullet_speed, dimensions, high_precision, args):
        if not self.calcCd(args):
            return False
        bullet = str(bullet_type)
        
        bullets.fire(bullet, [x + round(width / 2), y], dimensions,
                        IMG_ASSETS, bullet_speed, game_screen, bullet_type, mb.Mov_LinearFall())
        return True

class Shoot_Double(AbstractShoot):
    def Shoot(self,  bullets, IMG_ASSETS, game_screen, bullet_type, x, y, width, bullet_speed, dimensions, high_precision,args):
        if not  self.calcCd(args):
            return False
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
        return True

class Shoot_Triple(AbstractShoot):
    center_shoot = Shoot_Basic.Shoot
    def Shoot(self,  bullets, IMG_ASSETS, game_screen, bullet_type, x, y, width, bullet_speed, dimensions, high_precision,args):
        if not  self.calcCd(args):
            return False
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
        self.center_shoot(bullets, IMG_ASSETS, game_screen, bullet_type, x, y, width, bullet_speed, dimensions, high_precision,args)
        return True
class Shoot_Spread_Triple(AbstractShoot):

    center_shoot = Shoot_Basic.Shoot
    def Shoot(self,  bullets, IMG_ASSETS, game_screen, bullet_type, x, y, width, bullet_speed, dimensions, high_precision,args):
        if not self.calcCd(args):
            return False
        bullet = str(bullet_type)
        bullets.fire(bullet, [x + round(width * 0.1), y], dimensions,
                        IMG_ASSETS, bullet_speed, game_screen, bullet_type,  mb.Mov_DiagLeft(.7))

        bullets.fire(bullet, [x + round(width * 0.7), y], dimensions,
                        IMG_ASSETS, bullet_speed, game_screen, bullet_type,  mb.Mov_DiagRight(.7))

        self.center_shoot(bullets, IMG_ASSETS, game_screen, bullet_type, x, y, width, bullet_speed, dimensions, False,args)
        return True


class Shoot_Charging_Laser(AbstractShoot):
    center_shoot = Shoot_Basic.Shoot
    max_charge = 30
    def Shoot(self,  bullets, IMG_ASSETS, game_screen, bullet_type, x, y, width, bullet_speed, dimensions, high_precision, args):
        
        if args["charging"] <= self.max_charge:
            percent = args["charging"] / self.max_charge
            game_screen.drawListRect.append({"color": (235, 225, 225) , "coord": (x, y, 40, 8)} )
            game_screen.drawListRect.append({"color": (245, 22, 22) , "coord": (x, y, round(40 * percent) , 8)} )
            
            return True

        else:
            bullet = str(bullet_type)
            if bullet_type == ColorEnum.ColorEnum.Light:
                bullet_type = "laser light"
            else:
                bullet_type = "laser dark"
            bullets.fire(bullet, [x + round(width / 2), y], dimensions,
                            IMG_ASSETS, bullet_speed*0.6, game_screen, bullet_type,  mb.Mov_LinearFall())

            

           
            return True

