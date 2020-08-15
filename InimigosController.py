
from Droplet import Droplet
from enum import Enum
from copy import copy
class Inimigos:
    class EnumFormations(Enum):
        LINE = 1
        V = 2
    FORMATIONS = ["line","V"]

    def __init__(self):
        self.INIMIGOS = []

    def criar(self,key, coordinates, dimensions, speed, acceleration, IMG_ASSETS):
        self.INIMIGOS.append(Droplet(key, coordinates, dimensions, speed, acceleration, IMG_ASSETS))

    def mover(self, game_screen, dt):
        for i in self.INIMIGOS:
            i.fall(dt)
            if i.y + i.height > game_screen.height or i.health < 0:
                self.INIMIGOS.remove(i)

    def draw(self,game_screen):
        for i in self.INIMIGOS:
            i.draw(game_screen)

    def resize(self,game_screen):
        for i in self.INIMIGOS:
            i.resize(game_screen)

    def criarSwarm(self, type, quant, key, startcoordinates, space, dimension, speed, acceleration, IMG_ASSETS, SCALE_ASSETS):
        img_dim = (IMG_ASSETS[key].get_width(),IMG_ASSETS[key].get_height()) #pega a dimensão do asset
        scale = SCALE_ASSETS[key]

        cord = self.__coordenadaTipo(type, quant, space, startcoordinates, dimension, img_dim, scale) 
        
        for c in cord:
            self.INIMIGOS.append(Droplet(key, c, dimension, speed, acceleration, IMG_ASSETS))

        pass

    #tenta gerar coordenadas para os inimigos, com base nos parametros
    def __coordenadaTipo(self, type, quant, space, startcoordinates, screen_dim, img_dim, scale):
        cord = []
        scaleDim = (img_dim[0] * scale, img_dim[1] * scale)
        if type == self.EnumFormations.LINE:
            x, y = startcoordinates
            for i in range(0,quant):
                cord.append([x,y])
                x+=space + scaleDim[0]
                if (x + scaleDim[0]) >= screen_dim[0]:
                    break
        
        if type == self.EnumFormations.V:
            x, y = startcoordinates
            xe = copy(x)
            xd = copy(x)
            if (quant%2) == 1:
                quant-=1
                if (x + scaleDim[0]) <= screen_dim[0]:
                    cord.append([x,y])
                    y -= space

            for i in range(0,quant,2):
                if (xd + scaleDim[0]) <= screen_dim[0]:
                    xd +=  scaleDim[0]
                    cord.append([xd,y])
                    xd += space
                   
            
                if (xe - scaleDim[0]) >= 0:
                    xe -= scaleDim[0]
                    cord.append([xe,y])
                    xe -= space
                    
                
                y -= space

        return cord

    
        
