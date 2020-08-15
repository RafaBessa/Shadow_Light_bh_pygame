import pygame
import MovimentoMob as mm
import random


class GameMaster:
    def __init__(self, IMG_ASSETS, SCALE_ASSETS):
        self.lvl = 0
        self.movs = [mm.Mov_LinearFall(), mm.Mov_ZigZag()]
        self.form = [1, 2]
        self.quant = [i + 1 for i in range(20)]
        self.keys = ["roundguy"]
        self.ASSETS = IMG_ASSETS
        self.SCALE = SCALE_ASSETS
        self.speed = 2
        self.acceleration = .1

    def detect_state(self, inimigos, game_screen):
        if len(inimigos.INIMIGOS) == 0:
            self.next_level(inimigos, game_screen)
            print('SPICY')
        else:
            return inimigos

    def next_level(self, inimigos, game_screen):
        self.lvl += 1
        self.quant = [i + 1 for i in self.quant]
        self.speed = self.speed * 1.01

        for i in range(self.lvl):
            inimigos = self.more(inimigos, game_screen)
        return inimigos

    def more(self, inimigos, game_screen):
        formation = random.choice(self.form)
        key = random.choice(self.keys)
        quant = random.choice(self.quant)
        mov = random.choice(self.movs)
        startcoordinates = [250, 0]
        space = 20
        speed = random.triangular(self.speed - 1, self.speed, self.speed + 1)
        acceleration = self.acceleration

        inimigos.criarSwarm(formation, quant, key, startcoordinates, space, game_screen.shape, speed,
                            acceleration, self.ASSETS, self.SCALE, mov)

        return inimigos
