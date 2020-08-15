
from Droplet import Droplet

class Inimigos:
   
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
      