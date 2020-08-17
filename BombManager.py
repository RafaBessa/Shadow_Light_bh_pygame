from time import time

import pygame


class SpriteSheet:
    def __init__(self, filename, cells):
        self.sheet = pygame.image.load(filename).convert_alpha()
        self.cells = cells
        self.ncells = len(cells)

    def draw(self, surface, cellIndex, x, y):
        surface.blit(self.sheet, (x, y), self.cells[cellIndex])


celulas = [(0, 0, 100, 100),
           (100, 0, 100, 100),
           (200, 0, 100, 100),
           (300, 0, 100, 100),
           (400, 0, 100, 100),
           (500, 0, 100, 100),
           (600, 0, 100, 100),
           (700, 0, 100, 100),
           (800, 0, 100, 100),
           (900, 0, 100, 100),
           (0, 100, 100, 100),
           (100, 100, 100, 100),
           (200, 100, 100, 100),
           (300, 100, 100, 100),
           (400, 100, 100, 100),
           (500, 100, 100, 100),
           (600, 100, 100, 100),
           (700, 100, 100, 100),
           (800, 100, 100, 100),
           (900, 100, 100, 100),
           (0, 200, 100, 100),
           (100, 200, 100, 100),
           (200, 200, 100, 100),
           (300, 200, 100, 100),
           (400, 200, 100, 100),
           (500, 200, 100, 100),
           (600, 200, 100, 100),
           (700, 200, 100, 100),
           (800, 200, 100, 100),
           (900, 200, 100, 100),
           (0, 300, 100, 100),
           (100, 300, 100, 100),
           (200, 300, 100, 100),
           (300, 300, 100, 100),
           (400, 300, 100, 100),
           (500, 300, 100, 100),
           (600, 300, 100, 100),
           (700, 300, 100, 100),
           (800, 300, 100, 100),
           (900, 300, 100, 100),
           (0, 400, 100, 100),
           (100, 400, 100, 100),
           (200, 400, 100, 100),
           (300, 400, 100, 100),
           (400, 400, 100, 100),
           (500, 400, 100, 100),
           (600, 400, 100, 100),
           (700, 400, 100, 100),
           (800, 400, 100, 100),
           (900, 400, 100, 100),
           (0, 500, 100, 100),
           (100, 500, 100, 100),
           (200, 500, 100, 100),
           (300, 500, 100, 100),
           (400, 500, 100, 100),
           (500, 500, 100, 100),
           (600, 500, 100, 100),
           (700, 500, 100, 100),
           (800, 500, 100, 100),
           (900, 500, 100, 100),
           (0, 600, 100, 100),
           (100, 600, 100, 100),
           (200, 600, 100, 100),
           (300, 600, 100, 100),
           (400, 600, 100, 100),
           (500, 600, 100, 100),
           (600, 600, 100, 100),
           (700, 600, 100, 100),
           (800, 600, 100, 100),
           (900, 600, 100, 100),
           (0, 700, 100, 100)]

window = pygame.display.set_mode((100, 100))
pygame.display.set_caption("Sprite test")
sprite = SpriteSheet("assets\spritesheet.png", celulas)

run = True
FPS: int = 2  # a real é algo como 50 +- 10
clock = pygame.time.Clock()
t0 = time()
index = 0
while run:
    clock.tick(FPS)
    dt = time() - t0

    sprite.draw(window, index % sprite.ncells, 0, 0)
    pygame.display.update()

    if dt > 10:
        run = False
        pygame.quit()
    index += 1
