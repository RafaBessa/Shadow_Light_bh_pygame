import os
import pygame  # ver 1.9.6
from time import time

from Bullets import Bullets
from Player import Player
from Droplet import Droplet
from Window import Window
from InimigosController import Inimigos
# Default dimensions
DEFAULT_WINDOW_SIZES = [(1120, 580), (1680, 870)]
default_width, default_height = DEFAULT_WINDOW_SIZES[0]

# Background
BACKGROUND = pygame.image.load(os.path.join("assets", "background.png"))
BG_W, BG_H = BACKGROUND.get_width(), BACKGROUND.get_height()

IMG_ASSETS = {"ship1": pygame.image.load(os.path.join("assets", "ship1.png")),
              "roundguy": pygame.transform.rotate(pygame.image.load(os.path.join("assets", "roundguy.png")), 180),
              "red bullet": pygame.transform.rotate(pygame.image.load(os.path.join("assets", "red bullet.png")), 180)}
SCALE_ASSETS = {"ship1": .5,
                "roundguy": .3,
                "red bullet": .5}



def collide(obj1, obj2):
    return obj1.mask.overlap(obj2.mask, (obj2.x - obj1.x, obj2.y - obj1.y)) is not None


def main():
    FPS: int = 60
    clock = pygame.time.Clock()
    t0 = time()
    # Initializing window
    game_screen = Window("Shadow Light", DEFAULT_WINDOW_SIZES, BACKGROUND, SCALE_ASSETS, IMG_ASSETS)

    # Player
    player_fire_key = "red bullet"
    player_bullet_speed = -8
    player_speed = 4
    player = Player("ship1", [500, 460], game_screen.shape, player_speed,
                    IMG_ASSETS, player_fire_key, player_bullet_speed)
    player.draw(game_screen)

    # Enemies
    inimigos = Inimigos()
    inimigos.criar("roundguy", [400, 0], game_screen.shape, 0.5, 1, IMG_ASSETS)

    # Bullets
    bullets = Bullets([], IMG_ASSETS)

    #droplet.draw(game_screen)

    def redraw():
        game_screen.blit()
        player.draw(game_screen)
        inimigos.draw(game_screen)
        bullets.draw(game_screen)
        pygame.display.update()

    run = True
    while run:
        redraw()
        clock.tick(FPS)
        dt = time() - t0
        t0 = time()
        # TODO: Delete this print after testing:
        #if collide(player, inimigos.INIMIGOS[0]):
        #    print('ouch')

        # EVENTS
        for event in pygame.event.get():
            # CLOSE BUTTON
            if event.type == pygame.QUIT:
                run = False
            # RESIZE
            elif event.type == pygame.VIDEORESIZE and not game_screen._fullscreen:
                game_screen.resize(event.w, event.h)
                player.resize(game_screen)
                # inimigos.resize(game_screen)

        key = pygame.key.get_pressed()
        # CHANGING BETWEEN DEFAULT SIZES
        if key[pygame.K_MINUS] or key[pygame.K_EQUALS]:
            game_screen.resizeToDefault(key[pygame.K_EQUALS] - key[pygame.K_MINUS])  # next size
            player.resize(game_screen)
        if key[pygame.K_F11]:
            game_screen.toggleFullscreen()

        # AFTER CHANGING THE SCREEN
        # Player
        player.walk(key, game_screen, dt)
        if key[pygame.K_SPACE]:
            player.shoot(bullets,IMG_ASSETS)
        # Enemies
        inimigos.mover(dt)
        # Bullets
        bullets.move(dt)

    pygame.quit()


main()
