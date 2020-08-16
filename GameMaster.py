import pygame
import MovimentoMob as mm
import random
from ColorEnum import ColorEnum

class GameMaster:
    def __init__(self, IMG_ASSETS, SCALE_ASSETS):
        self.lvl = 0
        self.movs = [mm.Mov_LinearFall(), mm.Mov_ZigZag()]
        self.quant = [2]
        self.Bkeys = ["roundguy", "zag"]
        self.Wkeys = ["white"]
        self.cooldowns = [0.1,0.2,0.3,0.4,0.5]
        self.colors = [ColorEnum.Light,ColorEnum.Shadow]
        self.ASSETS = IMG_ASSETS
        self.SCALE = SCALE_ASSETS
        self.speed = 2
        self.acceleration = .1

    def detect_state(self, inimigos, shape):
        if len(inimigos.INIMIGOS) == 0:
            self.next_level(inimigos, shape)
            return inimigos
        else:
            return inimigos

    def next_level(self, inimigos, shape):
        self.lvl += 1
        self.quant = [i + 1 for i in self.quant]
        self.speed = self.speed * 1.1

        for i in range(self.lvl):
            inimigos = self.more(inimigos, shape)
        return inimigos

    def more(self, inimigos, shape):
        formation = random.choice([inimigos.EnumFormations.V, inimigos.EnumFormations.LINE])
        #key = random.choice(self.keys)
        quant = random.choice(self.quant)
        mov = random.choice(self.movs)
        startcoordinates = [random.randrange(0, shape[0]), random.randrange(-round(shape[1]*self.lvl/2), 0)]
        color = random.choice(self.colors)
        if color == ColorEnum.Light:
            key = random.choice(self.Wkeys)
        else:
            key = random.choice(self.Bkeys)
        space = 40
        speed = random.triangular(self.speed - 1, self.speed, self.speed + 1)
        acceleration = self.acceleration
        cd = random.choice(self.cooldowns)
        cd = random.triangular(cd-0.1,cd,cd+0.1)
        inimigos.criarSwarm(formation, quant, key, startcoordinates, space, shape, speed,
                            acceleration, self.ASSETS, self.SCALE, color, mov)

        return inimigos
