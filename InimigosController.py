
from Droplet import Droplet

class Inimigos:
   
    def __init__(self):
        self.INIMIGOS = []
    def criar(self,key, coordinates, dimensions, speed, acceleration, IMG_ASSETS):
        self.INIMIGOS.append(Droplet(key, coordinates, dimensions, speed, acceleration, IMG_ASSETS))

    def mover(self,dt):
        for i in self.INIMIGOS:
            i.fall(dt)

    def draw(self,game_screen):
        for i in self.INIMIGOS:
            i.draw(game_screen)
      