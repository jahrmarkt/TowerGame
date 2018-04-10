'''
erzeugt den code für die tower
damit ich nicht den code für die tower programmieren muss
'''


class DataBase(object):
    def __init__(self):
        self.output = ""

        self.towerNames = []
        self.ranges = []
        self.shootTimes = []
        self.isBoostings = []
        self.projectileTypes = []
        self.boostTypes = []

        self.projectileNames = []
        self.projSpeeds = []
        self.projDamages = []

        self.boostNames = []

    def addAttackTower(self, name, range, shootTime, projType):
        self.towerNames.append(name)
        self.ranges.append(range)
        self.shootTimes.append(shootTime)
        self.isBoostings.append(False)
        self.projectileTypes.append(projType)
        self.boostTypes.append(None)

    def addBoostTower(self, name, boostType):
        self.towerNames.append(name)
        self.ranges.append(10)
        self.shootTimes.append(10)
        self.isBoostings.append(True)
        self.projectileTypes.append(None)
        self.boostTypes.append(boostType)

    def addProjectile(self, name, speed, damage):
        self.projectileNames.append(name)
        self.projSpeeds.append(speed)
        self.projDamages.append(damage)

    def generateOutput(self):
        #0. header
        self.output += \
"""
from enum import Enum
from pygame.sprite import *


pygame.init()
pygame.mixer.init()
size = (width, height) = 512, 704
screen = pygame.display.set_mode(size)

def loadTower(n):
    filename = "assets/sprites/towers/" + n + ".png"
    
    return pygame.image.load(filename).convert_alpha()

def loadProjectile(n):
    filename = "assets/sprites/projectiles/" + n + ".png"
    return pygame.image.load(filename).convert_alpha()
    
class BoostType(Enum):
    SPEED = 1
    DAMAGE = 2
    RANGE = 3
    DOUBLE = 4
    
"""


        # 1. towerType
        self.output += "class TowerType(Enum):" + "\n"
        for index, name in enumerate(self.towerNames):
            self.output += "\t" + name.upper() + " = " + str(index) + "\n"
        self.output += "\n\n"

        # 5.projectileType
        self.output += "class ProjectileType(Enum):" + "\n"
        for index, name in enumerate(self.projectileNames):
            self.output += "\t" + name.upper() + " = " + str(index) + "\n"
        self.output += "\n\n"

        # 2. sprites Tower
        for index, name in enumerate(self.towerNames):
            self.output += "spriteTower" + name.title() + " = " + "loadTower('" + name + "')\n"
        self.output += "\n\n"

        # 3. icons Tower
        for index, name in enumerate(self.towerNames):
            self.output += "iconTower" + name.title() + " = " + "pygame.transform.scale(loadTower('" + name + "'), (64,64))\n"
        self.output += "\n\n"

        # 7. sprites Projectiles
        for index, name in enumerate(self.projectileNames):
            self.output += "spriteProjectile" + name.title() + " = " + "loadProjectile('" + name + "')\n"
        self.output += "\n\n"

        # 4.towerList
        self.output += "towerList = \\\n{"
        for i, name in enumerate(self.towerNames):
            self.output += \
                "\tTowerType." + name.upper() + " : (spriteTower" + name.title() + ", " + \
                str(self.ranges[i]) + ", " + \
                str(self.shootTimes[i]) + ", " + \
                str(self.isBoostings[i]) + ", " + \
                ("None" if self.projectileTypes[i] == None \
                else "ProjectileType." + str(self.projectileTypes[i]).upper()) + ", " + \
                ("None" if self.boostTypes[i] == None \
                else "BoostType." + str(self.boostTypes[i]).upper()) + ", " + \
                "iconTower" + name.title() + ")"
            self.output += ", \n"
        self.output += "}\n\n\n"

        # 4.projectileList
        self.output += "projectileList = \\\n{"
        for i, name in enumerate(self.projectileNames):
            self.output += \
                "\tProjectileType." + name.upper() + " : (spriteProjectile" + name.title() + ", " + \
                str(self.projSpeeds[i]) + ", " + \
                str(self.projDamages[i]) + ", " + ")"
            self.output += ", \n"

        self.output += "}\n\n"

    def saveFile(self):
        filename = "towerData.py"
        f = open(filename, "w")
        f.write(self.output)


data = DataBase()

#(spr, range, shoottime)
data.addAttackTower("fire", 100, 15, "fire")
data.addAttackTower("rocky", 150, 30, "arrow")
data.addAttackTower("yellow", 150, 30, "lightning1")
data.addAttackTower("green", 150, 30, "poison")
data.addAttackTower("redroof", 150, 30, "arrow")



data.addBoostTower("high", "damage")
data.addBoostTower("highblue", "range")
data.addBoostTower("highbrown", "range")
data.addBoostTower("rockyboost", "damage")
data.addBoostTower("library", "double")


#(spr, speed, damage)
data.addProjectile("fire", 3, 4)
data.addProjectile("lightning1", 2,1)
data.addProjectile("lightning2", 2,1)
data.addProjectile("arrow", 2,1)
data.addProjectile("poison", 3,1)
data.addProjectile("bomb", 1,1)



data.generateOutput()
data.saveFile()

print(data.output)
