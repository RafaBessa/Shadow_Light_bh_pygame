from MobPadrao import MobPadrao
from enum import Enum
from copy import copy
import MovimentoMob as mm
import PlayerShoot as PS


class Inimigos:
    class EnumFormations(Enum):
        LINE = 1
        V = 2

    def __init__(self):
        self.INIMIGOS = []

    def criar(self, key, coordinates, dimensions, speed, acceleration, IMG_ASSETS, bulletType, cd=0.5,
              mov_strat=mm.Mov_LinearFall(), life=1, shootStrategy=PS.Shoot_Basic()):
        self.INIMIGOS.append(
            MobPadrao(key, coordinates, dimensions, speed, acceleration, IMG_ASSETS, bulletType, mov_strat, cooldown=cd,
                      life=life, shootStrategy=shootStrategy))

    def mover(self, game_screen, dt):
        killNumbers = 0
        PassingNumber = 0
        for i in self.INIMIGOS:
            i.movimentar(dt)
            if i.y + i.height > game_screen.height:
                # inimigo saiu da tela
                PassingNumber += 1
                self.INIMIGOS.remove(i)
            elif i.health <= 0:
                # inimigo dead
                killNumbers += 1
                self.INIMIGOS.remove(i)
        return killNumbers, PassingNumber

    def draw(self, game_screen):
        for i in self.INIMIGOS:
            i.draw(game_screen)

    def resize(self, game_screen):
        for i in self.INIMIGOS:
            i.resize(game_screen)

    def shoot(self, bullets, IMG_ASSETS, game_screen):
        for i in self.INIMIGOS:
            i.shoot(bullets, IMG_ASSETS, game_screen)

    def criarSwarm(self, type, quant, key, startcoordinates, space, dimension, speed, acceleration, IMG_ASSETS,
                   SCALE_ASSETS, bullettype, mov_strategy=mm.Mov_LinearFall(), life=1, cd=0.5,
                   shootStrategy=PS.Shoot_Basic()):

        img_dim = (IMG_ASSETS[key].get_width(), IMG_ASSETS[key].get_height())  # pega a dimensão do asset
        scale = SCALE_ASSETS[key]

        cord = self.__coordenadaTipo(type, quant, space, startcoordinates, dimension, img_dim, scale)

        for c in cord:
            self.criar(key, c, dimension, speed, acceleration, IMG_ASSETS, bullettype, mov_strat=mov_strategy,
                       life=life, cd=cd, shootStrategy=shootStrategy)
        # self.INIMIGOS.append(MobPadrao(key, c, dimension, speed, acceleration, IMG_ASSETS))

    # tenta gerar coordenadas para os inimigos, com base nos parametros
    def __coordenadaTipo(self, type, quant, space, startcoordinates, screen_dim, img_dim, scale):
        cord = []
        scaleDim = (round(img_dim[0] * scale), round(img_dim[1] * scale))
        if type == self.EnumFormations.LINE:
            x, y = startcoordinates

            for i in range(0, quant):
                cord.append([x, y])
                x += space + scaleDim[0]
                if (x + scaleDim[0]) >= screen_dim[0]:
                    break

        if type == self.EnumFormations.V:
            x, y = startcoordinates
            xe = copy(x)
            xd = copy(x)
            if (quant % 2) == 1:
                quant -= 1
                if (x + scaleDim[0]) <= screen_dim[0]:
                    cord.append([x, y])
                    y -= space

            for i in range(0, quant, 2):
                if (xd + scaleDim[0]) <= screen_dim[0]:
                    xd += scaleDim[0]
                    cord.append([xd, y])
                    xd += space

                if (xe - scaleDim[0]) >= 0:
                    xe -= scaleDim[0]
                    cord.append([xe, y])
                    xe -= space

                y -= space

        return cord

    def get_bombed(self):
        for i in self.INIMIGOS:
            i.health -= 10


