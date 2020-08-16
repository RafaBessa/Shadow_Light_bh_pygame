from Entity import Entity
from ColorEnum import ColorEnum

class Bullets:
    def __init__(self, bullet_list, IMG_ASSETS):
        self.bullets = bullet_list

    def fire(self, key, coordinates, dimensions, IMG_ASSETS, speed, game_screen,type):
        if type == ColorEnum.Light:
            key = "light bullet"     
        else:
            key = "dark bullet"
        
        self.bullets.append(Bullet(key, coordinates, dimensions, IMG_ASSETS, speed, game_screen,type))

    def move(self, dt, game_screen):
        for bullet in self.bullets:
            bullet.move(dt)
            if not (0 < bullet.y < game_screen.height):
                self.bullets.remove(bullet)

    def resize(self, window):
        for bullet in self.bullets:
            bullet.resize(window)

    def draw(self, window):
        for i in self.bullets:
            i.draw(window)

    def hit(self, objs):

        for bullet in self.bullets:
            for obj in objs:
                if collide(bullet, obj):
                    obj.hit(bullet.dmg)
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)


class Bullet(Entity):
    def __init__(self, key, coordinates, dimensions, IMG_ASSETS, speed, game_screen,type):
        super().__init__(key, coordinates, dimensions, IMG_ASSETS )
        self.dmg = 1
        self._speed = speed
        self.speed = speed * self.img.get_width()
        self.resize(game_screen)
        self.type = type
    def move(self, dt):
        self.coordinates[1] = round(self.coordinates[1] + self.speed * dt)

    def resize(self, window):
        super().resize(window)
        self.speed = self._speed * self.img.get_height()


def collide(obj1, obj2):
    return obj1.mask.overlap(obj2.mask, (obj2.x - obj1.x, obj2.y - obj1.y)) is not None
