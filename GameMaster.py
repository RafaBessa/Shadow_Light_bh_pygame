from copy import copy
from math import atan
import MovimentoMob as mm
import random
from ColorEnum import ColorEnum
import numpy as np
import PlayerShoot as PS


class WeightedRandomizer:
    def __init__(self, weights):
        self.__max = .0
        self.__weights = []
        for value, weight in weights.items():
            self.__max += weight
            self.__weights.append((self.__max, value))

    def random(self):
        r = random.random() * self.__max
        for ceil, value in self.__weights:
            if ceil > r: return value


class GameMaster:
    def __init__(self, IMG_ASSETS, SCALE_ASSETS):
        self.lvl = 0
        self.movs = [mm.Mov_LinearFall(), mm.Mov_ZigZag()]
        self.boss_movs = [mm.Mov_HorizontalBossLeft(), mm.Mov_HorizontalBossRight()]
        self.quant = [2]
        self.Bkeys = ["roundguy", "zag"]
        self.Wkeys = ["white"]
        self.boss_Bkeys = ["roundguy B"]
        self.boss_Wkeys = ["white B"]
        self.cooldowns = np.arange(0.5, 1.5, 0.05)

        self.player = None
        self.colors = [ColorEnum.Light, ColorEnum.Shadow]
        self.Multiple_keys = ["BBEG"]
        self.Component_key = {"BBEG": ['bbeg center', 'white left', 'blue right']}

        self.speed = lambda: 3.25 ** atan(atan(self.lvl)) + .25
        self.acceleration = .1

        self.ASSETS = IMG_ASSETS
        self.SCALE = SCALE_ASSETS
        self.bossFreq = 5
        self.bosscount = 0
        self.bossY = [50, 100, 150, 200]

        self.ShootType = {"Basic": PS.Shoot_Basic(),
                          "Double": PS.Shoot_Double(),
                          "Triple": PS.Shoot_Triple()}

        self.ShootTypeProb = {"Basic": 0.75,
                              "Double": 0.2,
                              "Triple": 0.05}

        self.LevelShootProbRearanger = {"Basic": -0.05,
                                        "Double": +0.035,
                                        "Triple": +0.015}

        self.assistBonus = {"shoot": 0.33,
                            "cd": 0.33,
                            "bulletspeed": 0.33}

    def detect_state(self, inimigos, shape):
        if len(inimigos.INIMIGOS) <= 3:
            self.next_level(inimigos, shape)
            return inimigos
        else:
            return inimigos

    def next_level(self, inimigos, shape):
        self.lvl += 1
        self.quant = [i + 1 for i in self.quant]

        if (self.lvl % 3 == 0):  # adiciona os assistentes
            if len(self.player.Assistents) < 2:
                self.player.CreateAssistente()
            else:
                wr = WeightedRandomizer(self.assistBonus)
                bonus = wr.random()

                if (bonus == "shoot"):
                    for a in self.player.Assistents:
                        if (a.killStreak + 1 < len(a._ShootType)):
                            a.killStreak += 1
                        else:
                            self.assistBonus["shoot"] = 0.0

                        a.shootStrategy = a._ShootType[a.killStreak]
                    print(bonus)
                elif (bonus == "cd"):
                    for a in self.player.Assistents:
                        a.cooldowns *= 0.9
                    print(bonus)
                elif (bonus == "bulletspeed"):
                    for a in self.player.Assistents:
                        a.bulletspeed *= 1.1
                    print(bonus)

        if self.ShootTypeProb["Basic"] > 0:
            for key in self.ShootTypeProb:
                self.ShootTypeProb[key] -= self.LevelShootProbRearanger[key]

        if (self.lvl % self.bossFreq) == 0:
            inimigos = self.spawboss(inimigos, shape)
        else:
            for i in range(self.lvl):
                inimigos = self.more(inimigos, shape)

        if 5 > self.lvl > 3 and random.random() > .5:
            self.spawnAglomerate(inimigos, shape)

        return inimigos

    def more(self, inimigos, shape):
        formation = random.choice([inimigos.EnumFormations.V, inimigos.EnumFormations.LINE])
        # key = random.choice(self.keys)
        quant = random.choice(self.quant)
        mov = random.choice(self.movs)
        startcoordinates = [random.randrange(0, shape[0]), random.randrange(-round(shape[1] * self.lvl / 2), 0)]
        color = random.choice(self.colors)
        if color == ColorEnum.Light:
            key = random.choice(self.Wkeys)
        else:
            key = random.choice(self.Bkeys)
        space = 40
        speed = self.speed()
        speed = random.triangular(low=speed - 1, mode=speed, high=speed + 1)
        acceleration = self.acceleration
        cd = random.choice(self.cooldowns)

        cd = random.triangular(cd - 0.1, cd, cd + 0.1)
        wr = WeightedRandomizer(self.ShootTypeProb)

        inimigos.criarSwarm(formation, quant, key, startcoordinates, space, shape, speed,
                            acceleration, self.ASSETS, self.SCALE, color, mov, cd=cd,
                            shootStrategy=self.ShootType[wr.random()])
        return inimigos

    def spawboss(self, inimigos, shape):
        self.bosscount += 1
        formation = inimigos.EnumFormations.LINE
        for color in self.colors:
            for x in range(self.bosscount):
                quant = 1
                mov = random.choice(self.boss_movs)
                startcoordinates = [random.randrange(0, shape[0]), random.choice(self.bossY)]
                if color == ColorEnum.Light:
                    key = random.choice(self.boss_Wkeys)
                else:
                    key = random.choice(self.boss_Bkeys)
                space = 40
                speed = random.choice(np.arange(0.1, 0.4, 0.01))
                acceleration = 0.1
                cd = random.choice(self.cooldowns)
                cd = random.triangular(cd - 0.1, cd, cd + 0.1)
                life = 5
                inimigos.criarSwarm(formation, quant, key, startcoordinates, space, shape, speed,
                                    acceleration, self.ASSETS, self.SCALE, color, mov, life * self.bosscount, cd=cd)
        return inimigos

    def spawnAglomerate(self, inimigos, shape):
        self.bosscount += 1
        formation = inimigos.EnumFormations.LINE
        key = random.choice(self.Multiple_keys)
        startcoordinates = [shape[0] / 2, 50]
        speed = 1
        acceleration = 0
        color = random.choice(self.colors)
        mov = mm.Mov_HorizontalAglom()
        life = 50
        cd = .4

        inimigos.criar(self.Component_key[key][0], copy(startcoordinates), shape, speed, acceleration, self.ASSETS,
                       color, mov_strat=mov,
                       life=life, cd=cd / 3, shootStrategy=PS.Shoot_Spread_Triple())

        startcoordinates[0] -= 58
        inimigos.criar(self.Component_key[key][1], copy(startcoordinates), shape, speed, acceleration, self.ASSETS,
                       ColorEnum.Light, mov_strat=mov,
                       life=life, cd=cd, shootStrategy=PS.Shoot_Spread_Triple())

        startcoordinates[0] += 220
        inimigos.criar(self.Component_key[key][2], copy(startcoordinates), shape, speed, acceleration, self.ASSETS,
                       ColorEnum.Shadow, mov_strat=mov,
                       life=life, cd=cd, shootStrategy=PS.Shoot_Spread_Triple())

        return inimigos
