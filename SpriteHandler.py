from time import time

import pygame


class SpriteSheet:
    def __init__(self, filename, rows, cols):
        self.sheet = pygame.image.load(filename).convert_alpha()

        self.cols = cols
        self.rows = rows
        self.totalCellCount = cols * rows

        self.rect = self.sheet.get_rect()
        w = self.cellWidth = self.rect.width / cols
        h = self.cellHeight = self.rect.height / rows
        hw, hh = self.cellCenter = (w / 2, h / 2)

        self.cells = list([(index % cols * w, 0, w, h) for index in range(self.totalCellCount)])
        print(self.cells)

    def draw(self, surface, cellIndex, x, y):
        surface.blit(self.sheet, (x, y), self.cells[cellIndex])


window = pygame.display.set_mode((750, 750))
pygame.display.set_caption("Sprite test")

sprite = SpriteSheet("assets\EnergyBall.png", 1, 9)

run = True
FPS: int = 1  # a real é algo como 50 +- 10
clock = pygame.time.Clock()
t0 = time()
index = 0
while run:
    clock.tick(FPS)
    dt = time() - t0

    sprite.draw(window, index % sprite.totalCellCount, 200, 200)
    pygame.display.update()

    if dt > 10:
        run = False
        pygame.quit()
    index += 1



