import pygame
import os


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

    def __init__(self, caption, DEFAULT_WINDOW_SIZES, BACKGROUND, SCALE_ASSETS, IMG_ASSETS ):
        # Initialize with the first default dimensions
        self._default = 0
        self._fullscreen = False
        self.borders = [0, 0]
        self.DEFAULT_WINDOW_SIZES = DEFAULT_WINDOW_SIZES
        width, height = self.DEFAULT_WINDOW_SIZES[self._default]
        self.BACKGROUND = BACKGROUND
        self.BG_W, self.BG_H = BACKGROUND.get_width(), BACKGROUND.get_height()
        self.SCALE_ASSETS = SCALE_ASSETS
        self.IMG_ASSETS = IMG_ASSETS
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
        self.background = pygame.transform.scale(self.BACKGROUND, (width, height))
        # Displaying
        self._screen.blit(self.background, (0, 0))
        pygame.display.update()

    def resizeToDefault(self, increment):
        # Switch to the next window size
        self._default += increment
        self.borders = (0, 0)
        # Index overflow
        if self._default == len(self.DEFAULT_WINDOW_SIZES):
            self._default = 0
        elif self._default == - (1 + len(self.DEFAULT_WINDOW_SIZES)):
            self._default = len(self.DEFAULT_WINDOW_SIZES) - 1

        width, height = self.DEFAULT_WINDOW_SIZES[self._default]
        self.resize(width, height)

    def resizedAsset(self, key, coordinates, dimensions):
        # Resize with to the same scale as the background
        xscale = self.SCALE_ASSETS[key] * (self.width - self.borders[0]) / self.BG_W
        yscale = self.SCALE_ASSETS[key] * (self.height - self.borders[1])/ self.BG_H

        width = round(self.IMG_ASSETS[key].get_width() * xscale)
        height = round(self.IMG_ASSETS[key].get_height() * yscale)

        coordinates = [round(self.width * coordinates[0] / dimensions[0]),
                       round(self.height * coordinates[1] / dimensions[1])]

        return pygame.transform.scale(self.IMG_ASSETS[key], (width, height)), coordinates

    def draw(self, img, coordinates):
        self._screen.blit(img, coordinates)

    def blit(self):
        self._screen.blit(self.background, (0, 0))
