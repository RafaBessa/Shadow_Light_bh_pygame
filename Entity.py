import pygame

class Entity:
    def __init__(self, key, coordinates, dimensions, IMG_ASSETS):
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
    def width(self):
        return self.img.get_width()

    @property
    def height(self):
        return self.img.get_height()

    @property
    def mask(self):
        return pygame.mask.from_surface(self.img)
    @property
    def x(self):
        return self.coordinates[0]
    @property
    def y(self):
        return self.coordinates[1]
