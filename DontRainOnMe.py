import os
import pygame  # ver 1.9.6
from time import time

import Player
import Droplet
import Window
# DISCLAIMER: GLaDOS art made by Nannerman, available at https://www.pixilart.com/

# Last updated: 08/08/2020 (day/month/year)

# This is meant as a simple demonstration of how to resize the window using pygame, but it is not how
# it should be generally implemented for games

# # Default dimensions
# DEFAULT_WINDOW_SIZES = [(1120, 580), (1680, 870)]
# default_width, default_height = DEFAULT_WINDOW_SIZES[0]

# # Background
# BACKGROUND = pygame.image.load(os.path.join("assets", "background.png"))
# BG_W, BG_H = BACKGROUND.get_width(), BACKGROUND.get_height()

# IMG_ASSETS = {"guy": pygame.image.load(os.path.join("assets", "guy.png")),
#               "droplet": pygame.image.load(os.path.join("assets", "droplet.png"))}
# SCALE_ASSETS = {"guy": .5,
#                 "droplet": 5}


def main():
    FPS: int = 60
    clock = pygame.time.Clock()
    t0 = time()
    # Initializing window
    game_screen = Window.Window("Don't Rain On Me")
    player = Player.Player("guy", (500, 460), game_screen.shape, 2)
    player.draw(game_screen)

    droplet = Droplet.Droplet("droplet", (500, 0), game_screen.shape, 10, 7)
    droplet.draw(game_screen)

    def redraw():
        game_screen.blit()
        player.draw(game_screen)
        droplet.draw(game_screen)
        pygame.display.update()

    run = True
    while run:
        redraw()
        clock.tick(FPS)
        dt = time() - t0
        t0 = time()

        # EVENTS
        for event in pygame.event.get():
            # CLOSE BUTTON
            if event.type == pygame.QUIT:
                run = False
            # RESIZE
            elif event.type == pygame.VIDEORESIZE and not game_screen._fullscreen:
                game_screen.resize(event.w, event.h)
                player.resize(game_screen)

        key = pygame.key.get_pressed()
        # CHANGING BETWEEN DEFAULT SIZES
        if key[pygame.K_MINUS] or key[pygame.K_EQUALS]:
            game_screen.resizeToDefault(key[pygame.K_EQUALS] - key[pygame.K_MINUS])  # next size
            player.resize(game_screen)
        if key[pygame.K_F11]:
            game_screen.toggleFullscreen()
        if key[pygame.K_e]:
            FPS = 10

        # AFTER CHANGING THE SCREEN
        player.walk(key, game_screen, dt)
        droplet.fall(dt)

    pygame.quit()


main()
