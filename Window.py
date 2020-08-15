import pygame
import os
# Default dimensions
DEFAULT_WINDOW_SIZES = [(1120, 580), (1680, 870)]
default_width, default_height = DEFAULT_WINDOW_SIZES[0]

# Background
BACKGROUND = pygame.image.load(os.path.join("assets", "background.png"))
BG_W, BG_H = BACKGROUND.get_width(), BACKGROUND.get_height()

SCALE_ASSETS = {"guy": .5,
                "droplet": 5}
IMG_ASSETS = {"guy": pygame.image.load(os.path.join("assets", "guy.png")),
              "droplet": pygame.image.load(os.path.join("assets", "droplet.png"))}

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
