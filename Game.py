# NECESSARY DISCLAIMERS AND ATTRIBUTIONS:
# Space ships and bullets were made using BizmasterStudios' "Spaceship Creation Kit" available on itch.io
# Available at https://bizmasterstudios.itch.io/spaceship-creation-kit at the time of writing (15/08/2020 - dd/mm/yyyy)

import os
import pygame  # ver 1.9.6
from time import time
from Bullets import Bullets
from Player import Player
from Window import Window
from InimigosController import Inimigos
import GameMaster as gm

pygame.font.init()
pygame.mixer.init()
# Default dimensions
DEFAULT_WINDOW_SIZES = [(1120, 580), (1680, 870)]
default_width, default_height = DEFAULT_WINDOW_SIZES[0]

# Background
BACKGROUND = pygame.image.load(os.path.join("assets", "background.png"))
BG_W, BG_H = BACKGROUND.get_width(), BACKGROUND.get_height()

IMG_ASSETS = {"ship dark": pygame.image.load(os.path.join("assets", "ship1.png")),
              "ship light": pygame.image.load(os.path.join("assets", "ship2.png")),
              "roundguy": pygame.transform.rotate(pygame.image.load(os.path.join("assets", "roundguy.png")), 180),
              "roundguy B": pygame.transform.rotate(pygame.image.load(os.path.join("assets", "roundguy B.png")), 180),
              "red bullet": pygame.image.load(os.path.join("assets", "red bullet.png")),
              "healthbar": pygame.image.load(os.path.join("assets", "healthbar.png")),
              "white": pygame.transform.rotate(pygame.image.load(os.path.join("assets", "white.png")), 180),
              "white B": pygame.transform.rotate(pygame.image.load(os.path.join("assets", "white striped.png")), 180),
              "dark bullet": pygame.image.load(os.path.join("assets", "dark bullet.png")),
              "light bullet": pygame.image.load(os.path.join("assets", "light bullet.png")),
              "zag": pygame.transform.rotate(pygame.image.load(os.path.join("assets", "zag.png")), 180),
              "hit light": pygame.image.load(os.path.join("assets", "hit light.png")),
              "hit dark": pygame.image.load(os.path.join("assets", "hit dark.png")),
              "asst dark": pygame.image.load(os.path.join("assets", "asst1.png")),
              "asst light": pygame.image.load(os.path.join("assets", "asst2.png")),
              "bbeg center": pygame.image.load(os.path.join("assets", "bbeg center.png")),
              "blue right": pygame.image.load(os.path.join("assets", "blue right.png")),
              "white left": pygame.image.load(os.path.join("assets", "white left.png"))}

SCALE_ASSETS = {"ship dark": .2,
                "ship light": .2,
                "roundguy": .2,
                "roundguy B": .2,
                "red bullet": .2,
                "healthbar": 1.6,
                "dark bullet": .2,
                "rlight bullet": .2,
                "zag": .2,
                "white": 1.5,
                "white B": 1.5,
                "light bullet": .2,
                "hit light": .2,
                "hit dark": .2,
                "asst dark": .1,
                "asst light": .1,
                "bbeg center": 1,
                "blue right": 0.4365079365079365,
                "white left": 0.4296875}


def RIP_framerate(framerate):
    s = 0
    for fps in framerate[1:-1]:
        s += fps
    mean = s / (len(framerate) - 2)
    s = 0
    for fps in framerate[1:-1]:
        s += (fps - mean) ** 2
    desvpad = (s / (len(framerate) - 2)) ** 0.5
    print("{:.1f}".format(mean), '+-', "{:.1f}".format(desvpad))


framerate = []


def main():
    FPS: int = 60  # a real é algo como 50 +- 10
    clock = pygame.time.Clock()
    t0 = time()

    lost_font = pygame.font.SysFont("Comic Sans", 70)
    lost_font_rgb = (231, 88, 152)
    lost = False
    lost_time = 0

    # Initializing window
    game_screen = Window("Shadow Light", DEFAULT_WINDOW_SIZES, BACKGROUND, SCALE_ASSETS, IMG_ASSETS)

    # Game master
    GM = gm.GameMaster(IMG_ASSETS, SCALE_ASSETS)

    # Player
    player_fire_key = "red bullet"
    player_bullet_speed = -20.0
    player_speed = 12
    player = Player([500, 460], game_screen.shape, player_speed, IMG_ASSETS,
                    player_fire_key, player_bullet_speed,window=game_screen)

    GM.player = player
    player.draw(game_screen)

    # Enemies
    inimigos = Inimigos()
    # inimigos.criar("roundguy", (400, 0), game_screen.shape, 0.5, 1, IMG_ASSETS)
    # inimigos.criarSwarm(
    #     inimigos.EnumFormations.V, 3, "roundguy", [250, 0], 20, game_screen.shape,
    #     2, 0.1, IMG_ASSETS, SCALE_ASSETS, bullettype = ColorEnum.Light , mov_strategy=mm.Mov_ZigZag()
    # )

    # Bullets
    player_bullets = Bullets([])
    enemy_bullets = Bullets([])

    def redraw():
        game_screen.blit()
        player.draw(game_screen)
        inimigos.draw(game_screen)
        player_bullets.draw(game_screen)
        enemy_bullets.draw(game_screen)
        if lost:
            lost_label = lost_font.render("Game Over", 1, lost_font_rgb)
            game_screen._screen.blit(lost_label,
                                     (game_screen.width / 2 - lost_label.get_width() / 2, game_screen.height / 2))
        pygame.display.update()

    run = True
    while run:
        redraw()
        clock.tick(FPS)
        dt = time() - t0
        t0 = time()
        # ACTUAL FRAMERATE
        # framerate.append(1/dt)
        # print(round(framerate[-1]))

        if player.health <= 0:
            lost = True
            lost_time += dt
            if lost_time > 10:
                run = False
            else:
                continue

        # EVENTS
        for event in pygame.event.get():
            # CLOSE BUTTON
            if event.type == pygame.QUIT:
                run = False
            # RESIZE
            elif event.type == pygame.VIDEORESIZE and not game_screen._fullscreen:
                game_screen.resize(event.w, event.h)
                player.resize(game_screen)
                inimigos.resize(game_screen)
                player_bullets.resize(game_screen)
                enemy_bullets.resize(game_screen)

        key = pygame.key.get_pressed()
        # CHANGING BETWEEN DEFAULT SIZES
        if key[pygame.K_MINUS] or key[pygame.K_EQUALS]:
            game_screen.resizeToDefault(key[pygame.K_EQUALS] - key[pygame.K_MINUS])  # next size
            player.resize(game_screen)
            inimigos.resize(game_screen)
            player_bullets.resize(game_screen)
            enemy_bullets.resize(game_screen)
        if key[pygame.K_F11]:
            game_screen.toggleFullscreen()

        # AFTER CHANGING THE SCREEN
        # Player
        player.high_precision = key[pygame.K_LSHIFT]

        player.move(key, game_screen, dt)

        if key[pygame.K_SPACE]:
            player.shoot(player_bullets, IMG_ASSETS, game_screen)
        if key[pygame.K_e]:
            player.ChangeColor(game_screen)

        # Enemies
        DeathCount, PassingCount = inimigos.mover(game_screen, dt)
        player.scoreUpdate(DeathCount, PassingCount)
        inimigos.shoot(enemy_bullets, IMG_ASSETS, game_screen)

        # Bullets
        enemy_bullets.move(dt, game_screen)
        enemy_bullets.hit([player])

        player_bullets.move(dt, game_screen)
        player_bullets.hit(inimigos.INIMIGOS)
        # New game state
        GM.detect_state(inimigos, game_screen.shape)
        inimigos.resize(game_screen)

    print(player.score)
    #RIP_framerate(framerate)

    pygame.quit()


main()
