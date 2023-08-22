import pygame


class Human(pygame.sprite.Sprite):
    def __init__(self, location, image, gold=False):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.location = location
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = location
        self.gold = gold
        self.down = False

    def rot_center(self, angle):
        if not self.down:
            self.image = pygame.transform.rotate(self.image, angle)
            center = (self.rect.centerx, self.rect.centery + 50)
            self.rect = self.image.get_rect(center=center)
            self.rect.center = center
            self.location = center
            self.mask = pygame.mask.from_surface(self.image)
            self.down = True


class Movement(Human):
    def __init__(self, location, gold):
        if not gold:
            image = "images/вправо (2).png"
        else:
            image = "images/вправо_с_золотом.png"
        super().__init__(location, image, gold)
        self.direction = 'r'

    def flip(self, direction):
        if direction != self.direction:
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.image.get_rect()
            self.rect.center = self.location
            self.mask = pygame.mask.from_surface(self.image)  # обновили маску после уменьшения картинки
            self.direction = direction


class Stand_Human(Human):
    def __init__(self, location):
        super().__init__(location, "images/стоит1.png")


class House(pygame.sprite.Sprite):
    def __init__(self, location):
        super().__init__()
        self.image = pygame.image.load("images/дом.png").convert_alpha()
        self.location = location
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = location


class Door(pygame.sprite.Sprite):
    def __init__(self, location):
        super().__init__()
        self.image = pygame.image.load("images/door.png").convert_alpha()
        self.location = location
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = location
        self.reduce_size(5.3)

    def reduce_size(self, to):
        self.image = pygame.transform.scale(
            self.image, (self.image.get_width() // to, self.image.get_height() // to)
        )
        self.rect = self.image.get_rect()
        self.rect.center = self.location


class Platform(pygame.sprite.Sprite):
    def __init__(self, location):
        super().__init__()
        self.image = pygame.image.load("images/платформа.png").convert_alpha()
        self.location = location
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = location
        self.reduce_size(3.5)

    def reduce_size(self, to):
        self.image = pygame.transform.scale(
            self.image, (self.image.get_width() // to, self.image.get_height() // to)
        )
        self.rect = self.image.get_rect()
        self.rect.center = self.location
        self.mask = pygame.mask.from_surface(self.image)  # обновили маску после уменьшения картинки


class Mini_platforms(pygame.sprite.Sprite):
    def __init__(self, location):
        super().__init__()
        self.image = pygame.image.load("images/миниплатформ.png").convert_alpha()
        self.location = location
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = location
        self.on_platform = False
        self.reduce_size(3.5)

    def reduce_size(self, to):
        self.image = pygame.transform.scale(
            self.image, (self.image.get_width() // to, self.image.get_height() // to)
        )
        self.rect = self.image.get_rect()
        self.rect.center = self.location
        self.mask = pygame.mask.from_surface(self.image)


class Boiler(pygame.sprite.Sprite):
    def __init__(self, location):
        super().__init__()
        self.image = pygame.image.load("images/котел.png").convert_alpha()
        self.location = location
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = location
        self.reduce_size(3.5)

    def reduce_size(self, to):
        self.image = pygame.transform.scale(
            self.image, (self.image.get_width() // to, self.image.get_height() // to)
        )
        self.rect = self.image.get_rect()
        self.rect.center = self.location


class Gold_coins(pygame.sprite.Sprite):
    def __init__(self, location):
        super().__init__()
        self.image = pygame.image.load("images/Монеты.png").convert_alpha()
        self.location = location
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = location
        self.reduce_size(4.5)

    def reduce_size(self, to):
        self.image = pygame.transform.scale(
            self.image, (self.image.get_width() // to, self.image.get_height() // to)
        )
        self.rect = self.image.get_rect()
        self.rect.center = self.location


class Background(pygame.sprite.Sprite):
    def __init__(self, width, height, x = 1.875, image = "images/Фон.jpg"):
        super().__init__()
        self.image = pygame.image.load(image)
        self.reduce_size( x)
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)  # расположение экрана по центру

    def reduce_size(self, to):
        self.image = pygame.transform.scale(
            self.image, (self.image.get_width() // to, self.image.get_height() // to)
        )
        self.rect = self.image.get_rect()


class Background_two(Background):
    def __init__(self, width, height):
        super().__init__(width, height, 1.3, "images/заднийфон.png")
        self.delta = 0



class Monster(pygame.sprite.Sprite):
    def __init__(self, location, image, live=1):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.location = location
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = location
        self.live = live
        self.bullet_shot = []


class Red_Monster(Monster):
    def __init__(self, location):
        super().__init__(location, "images/монстр.png")


class Big_Monster(Monster):
    def __init__(self, location):
        super().__init__(location, "images/bigmonster.png", 5)
        self.on_ground = False


class Guns(pygame.sprite.Sprite):
    def __init__(self, location, image):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.location = location
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = location
        self.direction = 'r'

    def reduce_size(self, to):
        self.image = pygame.transform.scale(
            self.image, (self.image.get_width() // to, self.image.get_height() // to)
        )
        self.rect = self.image.get_rect()
        self.rect.center = self.location
        self.mask = pygame.mask.from_surface(self.image)  # обновили маску после уменьшения картинки

    def flip(self, direction):
        if direction != self.direction:
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.image.get_rect()
            self.rect.center = self.location
            self.mask = pygame.mask.from_surface(self.image)  # обновили маску после уменьшения картинки
            self.direction = direction


class AK_47(Guns):
    def __init__(self, location):
        super().__init__(location, "images/калаш.png")
        self.reduce_size(15)


class Bullet(Guns):
    def __init__(self, location):
        super().__init__(location, "images/пуля.png")
        self.reduce_size(30)


class Fireball(Guns):
    def __init__(self, location):
        super().__init__(location, "images/fireball.png")
        self.reduce_size(10)
