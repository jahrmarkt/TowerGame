from enum import Enum
from pygame.sprite import *

pygame.init()
pygame.mixer.init()
size = (width, height) = 512, 704
screen = pygame.display.set_mode(size)


def loadTower(n):
    # filename = "C:/Users/marko/Desktop/fh/OO Skriptsprachen/sprites/towers/" + n + ".png"
    filename = "assets/sprites/towers/" + n + ".png"

    return pygame.image.load(filename).convert_alpha()


def loadProjectile(n):
    # filename = "C:/Users/marko/Desktop/fh/OO Skriptsprachen/sprites/projectiles/" + n + ".png"
    filename = "assets/sprites/projectiles/" + n + ".png"
    return pygame.image.load(filename).convert_alpha()


class BoostType(Enum):
    SPEED = 1
    DAMAGE = 2
    RANGE = 3
    DOUBLE = 4


class TowerType(Enum):
    FIRE = 0
    ROCKY = 1
    YELLOW = 2
    GREEN = 3
    REDROOF = 4
    HIGH = 5
    HIGHBLUE = 6
    HIGHBROWN = 7
    ROCKYBOOST = 8
    LIBRARY = 9


class ProjectileType(Enum):
    FIRE = 0
    LIGHTNING1 = 1
    LIGHTNING2 = 2
    ARROW = 3
    POISON = 4
    BOMB = 5


spriteTowerFire = loadTower('fire')
spriteTowerRocky = loadTower('rocky')
spriteTowerYellow = loadTower('yellow')
spriteTowerGreen = loadTower('green')
spriteTowerRedroof = loadTower('redroof')
spriteTowerHigh = loadTower('high')
spriteTowerHighblue = loadTower('highblue')
spriteTowerHighbrown = loadTower('highbrown')
spriteTowerRockyboost = loadTower('rockyboost')
spriteTowerLibrary = loadTower('library')

iconTowerFire = pygame.transform.scale(loadTower('fire'), (64, 64))
iconTowerRocky = pygame.transform.scale(loadTower('rocky'), (64, 64))
iconTowerYellow = pygame.transform.scale(loadTower('yellow'), (64, 64))
iconTowerGreen = pygame.transform.scale(loadTower('green'), (64, 64))
iconTowerRedroof = pygame.transform.scale(loadTower('redroof'), (64, 64))
iconTowerHigh = pygame.transform.scale(loadTower('high'), (64, 64))
iconTowerHighblue = pygame.transform.scale(loadTower('highblue'), (64, 64))
iconTowerHighbrown = pygame.transform.scale(loadTower('highbrown'), (64, 64))
iconTowerRockyboost = pygame.transform.scale(loadTower('rockyboost'), (64, 64))
iconTowerLibrary = pygame.transform.scale(loadTower('library'), (64, 64))

spriteProjectileFire = loadProjectile('fire')
spriteProjectileLightning1 = loadProjectile('lightning1')
spriteProjectileLightning2 = loadProjectile('lightning2')
spriteProjectileArrow = loadProjectile('arrow')
spriteProjectilePoison = loadProjectile('poison')
spriteProjectileBomb = loadProjectile('bomb')

towerList = \
    {TowerType.FIRE: (spriteTowerFire, 100, 15, False, ProjectileType.FIRE, None, iconTowerFire),
     TowerType.ROCKY: (spriteTowerRocky, 150, 30, False, ProjectileType.ARROW, None, iconTowerRocky),
     TowerType.YELLOW: (spriteTowerYellow, 150, 30, False, ProjectileType.LIGHTNING1, None, iconTowerYellow),
     TowerType.GREEN: (spriteTowerGreen, 150, 30, False, ProjectileType.POISON, None, iconTowerGreen),
     TowerType.REDROOF: (spriteTowerRedroof, 150, 30, False, ProjectileType.ARROW, None, iconTowerRedroof),
     TowerType.HIGH: (spriteTowerHigh, 10, 10, True, None, BoostType.DAMAGE, iconTowerHigh),
     TowerType.HIGHBLUE: (spriteTowerHighblue, 10, 10, True, None, BoostType.RANGE, iconTowerHighblue),
     TowerType.HIGHBROWN: (spriteTowerHighbrown, 10, 10, True, None, BoostType.SPEED, iconTowerHighbrown),
     TowerType.ROCKYBOOST: (spriteTowerRockyboost, 10, 10, True, None, BoostType.DAMAGE, iconTowerRockyboost),
     TowerType.LIBRARY: (spriteTowerLibrary, 10, 10, True, None, BoostType.DOUBLE, iconTowerLibrary),
     }

projectileList = \
    {ProjectileType.FIRE: (spriteProjectileFire, 3, 4,),
     ProjectileType.LIGHTNING1: (spriteProjectileLightning1, 2, 1,),
     ProjectileType.LIGHTNING2: (spriteProjectileLightning2, 2, 1,),
     ProjectileType.ARROW: (spriteProjectileArrow, 2, 1,),
     ProjectileType.POISON: (spriteProjectilePoison, 3, 1,),
     ProjectileType.BOMB: (spriteProjectileBomb, 1, 1,),
     }
