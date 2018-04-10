from pygame.sprite import *
from pygame.locals import *
from pygame.mixer import *
from math import *
from random import randint
from enum import Enum

from TowerGame.version3.tower import *
from TowerGame.version3.towerData import *



# definitions
class Ground(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = loadSprite("grass" + str(randint(1, 4)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class City(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = spriteCity2
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.maxHealth = 200
        self.health = self.maxHealth


class Enemy(Sprite):
    def __init__(self, x, y, enemyType, sprite, speed, damage, health, ):
        Sprite.__init__(self)
        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vx = 0
        self.vy = speed
        self.x = x  # use this because img.rect.centerx is int and not float
        self.y = y

        self.enemyType = enemyType
        self.health = health
        self.speed = speed
        self.damage = damage

        self.onAttackPosition = False
        self.attackTimer = 0
        self.attackTime = 10

    def update(self):
        self.x += float(self.vx)
        self.y += float(self.vy)
        self.rect.centerx = self.x
        self.rect.centery = self.y
        if self.onAttackPosition:
            self.attackTimer = self.attackTimer + 1


# Level


# slot  = list of spawns
# spawn = (time, column, enemyType)
class LevelSlot(object):
    def __init__(self, spawns):
        self.spawns = spawns


class Level(object):
    def __init__(self):
        self.city = City(100, 100)
        self.slots = []
        self.slotTime = 20


# spawn = (time, column, enemyType)
def makeLevel1():
    level1 = Level()
    level1.city = City(232, 640)
    level1.slotTime = 10

    slots = [(0, 0), (1, 1), (2, 2), (3, 3), (2, 4), (1, 5), (0, 6), (4, 7)]
    slots2 = [(0, 2), (5, 3), (9, 4)]
    slots3 = [(0, 2), (0, 5)]
    slots4 = [(0, 2), (5, 5), (7, 9)]

    foo = lambda x: x + (EnemyType.NORMAL,)
    foo2 = lambda x: x + (EnemyType.BIG,)
    foo3 = lambda x: x + (EnemyType.HORSE,)
    foo4 = lambda x: x + (EnemyType.GHOST,)

    slots = list(map(foo, slots))
    slots2 = list(map(foo2, slots2))
    slots3 = list(map(foo3, slots3))
    slots4 = list(map(foo4, slots4))
    # try slot + EnemyType.NORMAL
    level1.slots = \
        [LevelSlot(slots)
            , LevelSlot(slots2)
            , LevelSlot(slots3)
            , LevelSlot(slots)
            , LevelSlot(slots2)
            , LevelSlot(slots)
            , LevelSlot(slots4)
            , LevelSlot(slots3)

         ]
    return level1


def spawnEnemies(level, time):
    time = time / 50
    enemies = []
    # get Slot and relative Time
    slotIndex = int(time / int(level.slotTime)) % len(level.slots)
    relTime = (time % level.slotTime)
    # print(slotIndex)

    slot = level.slots[slotIndex]

    # getSpawns and add them to Enemies
    for s in slot.spawns:
        (t, col, enemyType) = s
        (sprite, speed, damage, health) = enemyList[enemyType]
        if t == relTime:
            # Enemy(x,y,speed, damage, AttackTime)
            enemies.append(Enemy(col * 64 - 32, 0, enemyType, sprite, speed, damage, health))
    return enemies


class TowerMenuItem(Sprite):
    def __init__(self, x, y, image, towerType):
        Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.rect.size = 62, 62
        self.towerType = towerType


class TowerMenu(object):
    def __init__(self):
        self.items = []
        self.activeItemIndex = 0

        x = 448
        y = 0

        for index, key in enumerate(towerList):
            (spr, _, _, _, _, _, icon) = towerList[key]
            self.items.append(TowerMenuItem(x, y + index * 64, icon, key))

    def draw(self, screen):
        for index, it in enumerate(self.items):
            col = (0, 0, 0) if index != self.activeItemIndex else (0, 200, 0)
            pl = [it.rect.topleft, it.rect.topright, it.rect.bottomright, it.rect.bottomleft]
            pygame.draw.lines(screen, col, True, pl, 2)

        s = RenderPlain(self.items)
        s.draw(screen)

    def getTowerKey(self, cursor):
        for index, i in enumerate(self.items):
            if i.rect.collidepoint(cursor):
                self.activeItemIndex = index
                return self.items[self.activeItemIndex].towerType
        return None


class RandomTowerMenu(object):
    def __init__(self):
        self.items = []
        self.activeItemIndex = 0

        self.maxLength = 8
        self.x = 448  # topleft
        self.y = 0  # topleft

    def addRandomItem(self, input):
        if len(self.items) == self.maxLength:
            return

        index = randint(0, len(input) - 1)
        key = input[index]

        numItems = len(self.items)
        (spr, _, _, _, _, _, icon) = towerList[key]
        self.items.append(TowerMenuItem(self.x, self.y + numItems * 64, icon, key))
        self.activeItemIndex = numItems

    def addItem(self, key):
        if len(self.items) == self.maxLength:
            return

        numItems = len(self.items)
        (spr, _, _, _, _, _, icon) = towerList[key]
        self.items.append(TowerMenuItem(self.x, self.y + numItems * 64, icon, key))
        self.activeItemIndex = numItems

    def removeActiveItem(self):
        if (len(self.items) > 0):
            del self.items[self.activeItemIndex]
        # delete holes in list and reset position
        self.items = [item for item in self.items if item is not None]
        for index, item in enumerate(self.items):
            item.rect.y = self.y + index * 64

    def draw(self, screen):
        for index, it in enumerate(self.items):
            col = (0, 0, 0) if index != self.activeItemIndex else (0, 200, 0)
            pl = [it.rect.topleft, it.rect.topright, it.rect.bottomright, it.rect.bottomleft]
            pygame.draw.lines(screen, col, True, pl, 2)

        s = RenderPlain(self.items)
        s.draw(screen)

    def getTowerKey(self, cursor):
        for index, i in enumerate(self.items):
            if i.rect.collidepoint(cursor):
                self.activeItemIndex = index
                return self.items[self.activeItemIndex].towerType
        return None


# gerichter Graph
# pro Tower eine Liste von Connections die auf ihn zeigen
# nicht umgekehrt

class TowerGraph(object):
    def __init__(self):
        self.connections = []

    def addConnection(self, index, tower):
        self.connections[index].append(tower)

    def removeConnectionOfBoostTower(self, towerIndex):
        for index, c in enumerate(self.connections):
            self.connections[index] = list(filter(lambda x: x != towerIndex, c))

    def addTower(self):
        self.connections.append([])

    # !!! only call for non boost towers otherwise endless loop
    def getAllTowers(self, index):
        flatten = lambda l: [item for sublist in l for item in sublist]

        def getTowers(index):
            newTowers = self.connections[index]
            if not newTowers:
                return []
            else:
                return newTowers + flatten(map(getTowers, newTowers))

        return getTowers(index)


class Input(object):
    def __init__(self):
        self.mouseLeftPressed = False
        self.mouseRightPressed = False
        self.mouseLeftReleased = False
        self.cursor = (0, 0)
        self.returnKey = False
        self.timer = 0
        self.numberPressed = False
        self.numberKey = 0

    def reset(self):  # reset all except cursor
        self.mouseLeftPressed = False
        self.mouseRightPressed = False
        self.mouseLeftReleased = False
        self.returnKey = False
        self.timer = 0
        self.numberPressed = False
        self.numberKey = 0



def setCell(x, y, gridWidth, grid, v):
    grid[y * gridWidth + x] = v


def getCell(x, y, gridWidth, grid):
    return grid[y * gridWidth + x]


# enums
class CellType(Enum):
    FREE = 1
    OCCUPIED = 2
    FOUNDATION = 3
    CITY = 4


class EnemyType(Enum):
    NORMAL = 1
    BIG = 2
    HORSE = 3
    GHOST = 4


class GameState(Enum):
    RUN = 1
    RESTART = 2
    PAUSE = 3
    INTRO = 4


allTowerTypes = [TowerType.ROCKY, TowerType.FIRE, TowerType.ROCKY, TowerType.HIGH, TowerType.HIGHBLUE,
                 TowerType.ROCKYBOOST, TowerType.YELLOW, TowerType.LIBRARY]


class Model(object):
    def __init__(self, screenWidth, screenHeight):

        startLevel = makeLevel1()

        self.level = startLevel

        # tower menu
        self.towerMenu = RandomTowerMenu()
        for a in allTowerTypes:
            self.towerMenu.addItem(a)


            # self.towerMenu.addItem(TowerType.HIGHBLUE)
            # self.towerMenu.addItem(TowerType.HIGH)
            # self.towerMenu.addItem(TowerType.ROCKY)

        # Entities
        self.towers = []
        self.projectiles = []
        self.enemies = []
        self.effects = []
        self.city = startLevel.city

        # gameplay
        self.towerGraph = TowerGraph()
        self.spawnrate = 60
        self.towerSpawnRate = 1600
        self.towerSpawnTimer = 0
        self.enemiesCreated = 0
        self.enemiesKilled = 0
        self.boostRange = 150

        # game related
        self.gameState = GameState.RUN
        self.towerListKey = self.towerMenu.getTowerKey((450, 1))
        self.activeTower = None
        self.activeTowerIndex = None
        self.pressOnBoost = False  # for picking boost target
        self.lastPressPosition = None
        self.mouseLeftDown = False

        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        self.gridWidth = 7
        self.gridHeight = 11
        self.gridSize = 64
        self.groundSprites = []
        self.foundationImage = spriteFoundation3

        for x in range(14):
            for y in range(22):
                self.groundSprites.append(Ground(x * 32, y * 32))

        self.grid = []

        for x in range(self.gridWidth * self.gridHeight):
            self.grid.append(CellType.FREE)

        # set City
        setCell(2, 9, self.gridWidth, self.grid, CellType.CITY)
        setCell(3, 9, self.gridWidth, self.grid, CellType.CITY)
        setCell(4, 9, self.gridWidth, self.grid, CellType.CITY)
        setCell(2, 10, self.gridWidth, self.grid, CellType.CITY)
        setCell(3, 10, self.gridWidth, self.grid, CellType.CITY)
        setCell(4, 10, self.gridWidth, self.grid, CellType.CITY)

        # setStartFoundation
        #  setCell(2, 6, self.gridWidth, self.grid, CellType.FOUNDATION)
        setCell(2, 7, self.gridWidth, self.grid, CellType.FOUNDATION)
        setCell(3, 6, self.gridWidth, self.grid, CellType.FOUNDATION)
        #  setCell(3, 7, self.gridWidth, self.grid, CellType.FOUNDATION)

        #  setCell(4, 6, self.gridWidth, self.grid, CellType.FOUNDATION)
        setCell(4, 7, self.gridWidth, self.grid, CellType.FOUNDATION)



# assets

# Sprites

def loadSprite(n):
#    filename = "C:/Users/marko/Desktop/fh/OO Skriptsprachen/sprites/" + n + ".gif"
    filename = "assets/sprites/" + n + ".gif"
    return pygame.image.load(filename).convert_alpha()


def loadSprite2(n):
    #filename = "C:/Users/marko/Desktop/fh/OO Skriptsprachen/sprites/" + n + ".png"
    filename = "assets/sprites/" + n + ".png"
    return pygame.image.load(filename).convert_alpha()


spriteAttack = loadSprite("attack1")
spriteCity = loadSprite("city1")
spriteCity2 = pygame.transform.scale(loadSprite2("city1"), (3 * 64, 128))
spriteFoundation = loadSprite("foundation1")
spriteFoundation2 = loadSprite("foundation2")
spriteFoundation3 = loadSprite("foundation3")

spriteGrass1 = loadSprite("grass1")
spriteGrass2 = loadSprite("grass2")
spriteGrass3 = loadSprite("grass3")
spriteGrass4 = loadSprite("grass4")


# Animations

def loadAnimation(n, num):
    #foo = lambda index: "C:/Users/marko/Desktop/fh/OO Skriptsprachen/sprites/animations/" + n + str(index) + ".png"
    foo = lambda index: "assets/sprites/animations/" + n + str(index) + ".png"
    filenames = list(map(foo, range(1, num + 1)))
    images = []
    for n in filenames:
        images.append(pygame.image.load(n).convert_alpha())
    return images


animBoost1 = loadAnimation("boost", 6)
animBoost2 = loadAnimation("boosta", 1)
animBoost3 = loadAnimation("boostb", 2)
animBoost4 = loadAnimation("boostc", 15)
animExplosion1 = loadAnimation("explosion", 7)


# Sounds

def loadSound(n):
    #return pygame.mixer.Sound("C:/Users/marko/Desktop/fh/OO Skriptsprachen/sounds/" + n + ".wav")
    return pygame.mixer.Sound("assets/sounds/" + n + ".wav")


# Enemy
soundHit = loadSound("hit1")
soundCoin = loadSound("coin1")
soundTower = loadSound("setTower")
soundShoot = loadSound("shoot1")
soundExplosion1 = loadSound("explosion1")
soundHit2 = loadSound("hit2")
soundSelect1 = loadSound("select1")
soundPowerUp = loadSound("powerup2")

spriteEnemy = loadSprite("enemy2")
spriteEnemyBig = loadSprite("enemybig")
spriteEnemyGhost = loadSprite("enemyghost")
spriteEnemyHorse = loadSprite("enemyhorse")

# (sprite, speed, damage, health)
enemyList = \
    {EnemyType.NORMAL: (spriteEnemy, 0.8, 1, 5),
     EnemyType.BIG: (spriteEnemyBig, 0.1, 4, 15),
     EnemyType.HORSE: (spriteEnemyHorse, 0.6, 2, 3),
     EnemyType.GHOST: (spriteEnemyGhost, 0.3, 2, 3),
     }
