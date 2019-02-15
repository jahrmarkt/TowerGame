from pygame.sprite import *
from enum import Enum


# Helper

# must be all the same size
class AnimationLoop(Sprite):
    def __init__(self, x, y, images, frameTime, angle=0):
        Sprite.__init__(self)
        self.imageIndex = 0
        self.timer = 0
        self.frameTime = frameTime
        self.numImages = len(images)
        self.images = list(images)
        for img in images:
            self.images.append(pygame.transform.rotate(img, angle + 90))

        self.image = self.images[self.imageIndex]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.timer = self.timer + 1
        if self.timer == self.frameTime:
            self.timer = 0
            self.imageIndex = (self.imageIndex + 1) % self.numImages
            self.image = self.images[self.imageIndex]


# must be all the same size
class AnimationOnce(Sprite):
    def __init__(self, x, y, images, frameTime, angle=0):
        Sprite.__init__(self)
        self.imageIndex = 0
        self.timer = 0
        self.frameTime = frameTime
        self.numImages = len(images)
        self.images = list(images)
        for img in images:
            self.images.append(pygame.transform.rotate(img, angle + 90))

        self.image = self.images[self.imageIndex]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.done = False

    def update(self):
        if self.done:
            return

        self.timer = self.timer + 1
        if self.timer == self.frameTime:
            self.timer = 0
            self.imageIndex = self.imageIndex + 1
            if self.imageIndex == self.numImages:
                self.done = True
                return
            self.image = self.images[self.imageIndex]


# definitions
## unused currently
class Boost(AnimationLoop):
    def __init__(self, x, y, angle, anim, frameTime, boostType):
        AnimationLoop.__init__(self, x, y, anim, frameTime, angle)
        self.type = boostType

    def update(self):
        super().update()


class Projectile(Sprite):
    def __init__(self, x, y, angle, sprite, speed=1, damage=1, range=20):
        Sprite.__init__(self)
        self.image = pygame.transform.rotate(sprite, angle + 90)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vx = 0
        self.vy = 0
        self.x = x  # use this because img.rect.centerx is int and not float
        self.y = y

        self.damage = damage
        self.lifeTime = range / speed
        self.timer = 0
        self.range = range
        self.done = False

    def update(self):
        self.timer = self.timer + 1
        if self.timer >= self.lifeTime:
            self.done = True
        self.x += float(self.vx)
        self.y += float(self.vy)
        self.rect.centerx = self.x
        self.rect.centery = self.y


class Tower(Sprite):
    def __init__(self, x, y, spr, agroradius, shootTime, isBoostTower, projInfo, boostType):
        Sprite.__init__(self)
        # general
        self.image = spr
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.isBoostTower = isBoostTower

        # attack info
        self.agroradius = agroradius
        self.shootTime = shootTime
        self.shootTimer = False
        self.shootLock = False
        self.projInfo = projInfo

        # boost info
        self.boost = boostType  # boost this tower is sending

    def update(self):
        if self.isBoostTower:
            pass
        else:
            self.shootTimer = self.shootTimer + 1
            if self.shootTimer >= self.shootTime:
                self.shootTimer = 0
                self.shootLock = False
