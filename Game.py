import os
import pygame  # ver 1.9.6
from time import time

from Bullets import Bullets
from Player import Player
from MobPadrao import MobPadrao
from Window import Window
from InimigosController import Inimigos
import MovimentoMob as mm
import PlayerShoot as ps
import GameMaster as gm
from ColorEnum import ColorEnum

pygame.font.init()

# Default dimensions
DEFAULT_WINDOW_SIZES = [(1120, 580), (1680, 870)]
default_width, default_height = DEFAULT_WINDOW_SIZES[0]

# Background
BACKGROUND = pygame.image.load(os.path.join("assets", "background.png"))
BG_W, BG_H = BACKGROUND.get_width(), BACKGROUND.get_height()

IMG_ASSETS = {"ship1": pygame.image.load(os.path.join("assets", "ship1.png")),
              "roundguy": pygame.transform.rotate(pygame.image.load(os.path.join("assets", "roundguy.png")), 180),
              "red bullet": pygame.transform.rotate(pygame.image.load(os.path.join("assets", "red bullet.png")), 180),
              "healthbar": pygame.transform.rotate(pygame.image.load(os.path.join("assets", "healthbar.png")), 180),
              "dark bullet": pygame.transform.rotate(pygame.image.load(os.path.join("assets", "red bullet.png")), 180),
              "light bullet": pygame.transform.rotate(pygame.image.load(os.path.join("assets", "healthbar.png")), 180)}

SCALE_ASSETS = {"ship1": .2,
                "roundguy": .2,
                "red bullet": .2,
                "healthbar": 3,
                "dark bullet": .2,
                "light bullet": .2}

def main():
    FPS: int = 70
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
    player_bullet_speed = -10
    player_speed = 8
    player = Player("ship1", [500, 460], game_screen.shape, player_speed,
                    IMG_ASSETS, player_fire_key, player_bullet_speed, ps.Shoot_Basic())
    player.draw(game_screen)

    # Enemies
    inimigos = Inimigos()
    # inimigos.criar("roundguy", (400, 0), game_screen.shape, 0.5, 1, IMG_ASSETS)
    inimigos.criarSwarm(
        inimigos.EnumFormations.V, 3, "roundguy", [250, 0], 20, game_screen.shape,
        2, 0.1, IMG_ASSETS, SCALE_ASSETS, bullettype = ColorEnum.Light , mov_strategy=mm.Mov_ZigZag()
    )
    # inimigos.criar("roundguy", [400, 0], game_screen.shape, 0.5, 1, IMG_ASSETS)
    # inimigos.criar("roundguy", [400, 0], game_screen.shape, 0.5, 1, IMG_ASSETS)
    # inimigos.criar("roundguy", [400, 100], game_screen.shape, 0, 0, IMG_ASSETS)

    # Bullets
    player_bullets = Bullets([], IMG_ASSETS)
    enemy_bullets = Bullets([], IMG_ASSETS)

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

        if player.health <= 0:
            lost = True
            lost_time += dt
            if lost_time > 2:
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
        player.walk(key, game_screen, dt)
        if key[pygame.K_SPACE]:
            player.shoot(player_bullets, IMG_ASSETS, game_screen)
        if key[pygame.K_e]:
            player.ChangeColor()
            
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
       # inimigos = GM.detect_state(inimigos, (BG_W, BG_H))
        inimigos = GM.detect_state(inimigos, game_screen.shape)
        inimigos.resize(game_screen)
    pygame.quit()


main()
