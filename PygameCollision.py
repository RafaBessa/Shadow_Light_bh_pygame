import os
import pygame  # ver 1.9.6
from time import time

# DISCLAIMER: GLaDOS art made by Nannerman, available at https://www.pixilart.com/

# Last updated: 08/08/2020 (day/month/year)

# This is meant as a simple demonstration of how to resize the window using pygame, but it is not how
# it should be generally implemented for games

# Default dimensions
DEFAULT_WINDOW_SIZES = [(700, 580)]
default_width, default_height = DEFAULT_WINDOW_SIZES[0]

# Background
BACKGROUND = pygame.image.load(os.path.join("assets", "background.png"))
BG_W, BG_H = BACKGROUND.get_width(), BACKGROUND.get_height()

IMG_ASSETS = {"blue": pygame.image.load(os.path.join("assets", "blue.png")),
              "red": pygame.image.load(os.path.join("assets", "red.png"))}
SCALE_ASSETS = {"blue": 5,
                "red": .7}

class Window:
    @property
    def width(self):
        return self._screen.get_width()
    @property
    def height(self):
        return self._screen.get_height()
    @property
    def shape(self):
        return self._screen.get_width(), self._screen.get_height()

    def __init__(self, caption):
        # Initialize with the first default dimensions
        self._default = 0
        self._fullscreen = False
        self.borders = [0, 0]
        width, height = DEFAULT_WINDOW_SIZES[self._default]

        # Creating inner screen object
        self._screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption(caption)

        # Adjusting background
        self.background = pygame.transform.scale(BACKGROUND, (width, height))

        # Displaying background
        self._screen.blit(self.background, (0, 0))
        pygame.display.update()

    def toggleFullscreen(self):
        if self._fullscreen:
            self._screen = pygame.display.set_mode(self.shape, pygame.RESIZABLE)
        else:
            self._screen = pygame.display.set_mode(self.shape, pygame.FULLSCREEN)
        self._fullscreen = not self._fullscreen

    def resize(self, width, height):
        self._screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.background = pygame.transform.scale(BACKGROUND, (width, height))
        # Displaying
        self._screen.blit(self.background, (0, 0))
        pygame.display.update()

    def resizeToDefault(self, increment):
        # Switch to the next window size
        self._default += increment
        self.borders = (0, 0)
        # Index overflow
        if self._default == len(DEFAULT_WINDOW_SIZES):
            self._default = 0
        elif self._default == - (1 + len(DEFAULT_WINDOW_SIZES)):
            self._default = len(DEFAULT_WINDOW_SIZES) - 1

        width, height = DEFAULT_WINDOW_SIZES[self._default]
        self.resize(width, height)

    def resizedAsset(self, key, coordinates, dimensions):
        # Resize with to the same scale as the background
        xscale = SCALE_ASSETS[key] * (self.width - self.borders[0]) / BG_W
        yscale = SCALE_ASSETS[key] * (self.height - self.borders[1])/ BG_H

        width = round(IMG_ASSETS[key].get_width() * xscale)
        height = round(IMG_ASSETS[key].get_height() * yscale)

        coordinates = [round(self.width * coordinates[0] / dimensions[0]),
                       round(self.height * coordinates[1] / dimensions[1])]

        return pygame.transform.scale(IMG_ASSETS[key], (width, height)), coordinates

    def draw(self, img, coordinates):
        self._screen.blit(img, coordinates)

    def blit(self):
        self._screen.blit(self.background, (0, 0))


class Entity:
    def __init__(self, key, coordinates, dimensions):
        self.coordinates = coordinates
        self._dimensions = dimensions

        self.img_key = key
        self.img = IMG_ASSETS[key]

    def resize(self, window):
        self.img, self.coordinates = window.resizedAsset(self.img_key, self.coordinates, self._dimensions)
        self._dimensions = window.shape
        self.draw(window)

    def draw(self, window):
        window.draw(self.img, self.coordinates)

    @property
    def mask(self):
        return pygame.mask.from_surface(self.img)
    @property
    def x(self):
        return self.coordinates[0]
    @property
    def y(self):
        return self.coordinates[1]
    @property
    def width(self):
        return self.img.get_width()

    @property
    def height(self):
        return self.img.get_height()


class Player(Entity):

    def __init__(self, key, coordinates, dimensions, speed):
        super().__init__(key, coordinates, dimensions)
        self._speed = speed  # in widths per second
        self.speed = speed*self.img.get_width()

    def resize(self, window):
        super().resize(window)
        self.speed = self._speed * self.img.get_width()

    def move(self, key, window, dt):
        u = (key[pygame.K_d] - key[pygame.K_a])
        v = (key[pygame.K_s] - key[pygame.K_w])
        modulus = (u ** 2 + v ** 2) ** .5

        # Checks for simultaneous WS or AD presses
        if modulus > 0:
            # making linear velocity equal to player velocity
            modulus = self.speed * dt / modulus
            u = round(u * modulus)
            v = round(v * modulus)
            # Checking left border
            if self.coordinates[0] + u > 0:
                # Checking right border
                if self.coordinates[0] + u < window.width - self.width:
                    # Moving
                    self.coordinates[0] += u
                else:
                    # Hugging right
                    self.coordinates[0] = window.width - self.width
            else:
                # Hugging left
                self.coordinates[0] = 0

            # Checking upper border
            if self.coordinates[1] + v > 0:
                # Checking lower border
                if self.coordinates[1] + v < window.height - self.height:
                    # Moving
                    self.coordinates[1] += v
                else:
                    # Hugging lower border
                    self.coordinates[1] = window.height - self.height
            else:
                # Hugging upper border
                self.coordinates[1] = 0

def collide(obj1, obj2):
    # obj1.coordinate - obj2.coordinate does not work
    return obj1.mask.overlap(obj2.mask, (obj2.x - obj1.x, obj2.y - obj1.y)) is not None

def main():
    FPS: int = 60
    clock = pygame.time.Clock()
    t0 = time()
    # Initializing window
    game_screen = Window("Don't Rain On Me")
    player = Player("red", (500, 460), game_screen.shape, 2)
    player.draw(game_screen)

    blue = Entity("blue", (500, 460), game_screen.shape)
    blue.draw(game_screen)

    def redraw():
        game_screen.blit()
        player.draw(game_screen)
        blue.draw(game_screen)
        pygame.display.update()

    run = True
    while run:
        redraw()
        clock.tick(FPS)
        dt = time() - t0
        t0 = time()

        print((collide(player, blue),collide(blue, player)))

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

        # AFTER CHANGING THE SCREEN
        player.move(key, game_screen, dt)

    pygame.quit()


main()
