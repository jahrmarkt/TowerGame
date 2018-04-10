from TowerGame.version3.model import *


# Helper

def lenVector(x, y):
    return sqrt(x * x + y * y)


def normalizeVector(x, y):
    l = sqrt(x * x + y * y)
    if l == 0:
        l = 0.001
    return (x / l, y / l)


def partition(pred, data):
    yes, no = [], []
    for d in data:
        (yes if pred(d) else no).append(d)
    return (yes, no)


def uniq(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


# Game Logic

def moveEnemies(enemies, city, towers):
    for e in enemies:
        if e.onAttackPosition:
            pass
        elif e.rect.colliderect(city.rect):
            e.onAttackPosition = True
            e.vx = 0
            e.vy = 0
        elif e.rect.centery >= city.rect.y:
            e.vy = 0
            e.vx = e.speed if e.rect.centerx < city.rect.centerx else -e.speed


def collisionArrowsEnemies(arrows, enemies):
    numHits = 0
    for e in enemies:
        # check collision
        hit, miss = partition(lambda x: e.rect.colliderect(x.rect), arrows)
        numHits += len(hit)
        for a in hit:
            e.health -= a.damage
        arrows = miss
    return arrows, enemies, numHits


def shootArrows(towerGraph, towers, enemies, arrows):
    numArrows = 0
    for towerIndex, t in enumerate(towers):
        if not t.isBoostTower and not t.shootLock:

            boosts = uniq(map(lambda x: towers[x].boost, towerGraph.getAllTowers(towerIndex)))
            # print(boosts)

            multiplier = 1
            if BoostType.DOUBLE in boosts:
                multiplier = 2

            # apply range bonus
            agroradius = t.agroradius
            if BoostType.RANGE in boosts:
                agroradius = agroradius + (150 * multiplier)

            for e in enemies:
                if e.rect.colliderect(
                        Rect(t.rect.centerx - agroradius, t.rect.centery - agroradius, agroradius * 2,
                             agroradius * 2)):

                    # compute angle for projectile
                    tx = e.rect.centerx - t.rect.centerx
                    ty = e.rect.centery - t.rect.centery
                    angle = degrees(-(atan2(ty, tx) + pi / 2))
                    (spr, speed, damage) = t.projInfo

                    # apply damage bonus

                    if BoostType.DAMAGE in boosts:
                        damage = damage + (2 * multiplier)

                    newArrow = Projectile(t.rect.centerx, t.rect.centery, angle, spr, speed, damage, agroradius)
                    vx, vy = normalizeVector(tx, ty)
                    vx = float(vx * speed)
                    vy = float(vy * speed)
                    newArrow.vx = vx
                    newArrow.vy = vy
                    numArrows = numArrows + 1
                    arrows.append(newArrow)
                    t.shootLock = True
                    break
    return towers, arrows, numArrows


def attackCity(enemies, city):
    numAttacks = 0  # for animations
    for e in enemies:
        if e.onAttackPosition:
            if e.attackTimer % e.attackTime == 0:
                numAttacks = numAttacks + 1
                city.health -= e.damage
    return enemies, city, numAttacks


def outOfScreen(entities, screenwidth, screenheight):
    entities = list(filter(lambda x: x.rect.colliderect(0, 0, screenwidth, screenheight), entities))
    return entities


def clearProjectiles(projectiles, screenWidth, screenHeight):
    p = list(filter(lambda x: not x.done and x.rect.colliderect(0, 0, screenWidth, screenHeight), projectiles))
    return p


def clearEnemies(enemies, screenwidth, screenheight):
    alive, dead = list(partition(lambda x: x.health > 0, enemies))
    inside = list(filter(lambda x: x.rect.colliderect(0, 0, screenwidth, screenheight), alive))
    return inside, dead


# main function

def updateRun(input, screen, model):
    # input

    gameArea = Rect(0, 0, 448, 704)

    if input.returnKey:
        model.gameState = GameState.PAUSE
        return

    if input.mouseLeftReleased and gameArea.collidepoint(input.cursor):
        if model.pressOnBoost:
            # print("press Released")
            # check if inside boostrange
            (cx, cy) = input.cursor
            (ax, ay) = model.activeTower.rect.center
            tx = ax - cx
            ty = ay - cy
            if lenVector(tx, ty) < model.boostRange:

                # find tower and set boostTarget
                for index, newTower in enumerate(model.towers):
                    if newTower.rect.collidepoint(input.cursor):
                        # print("found tower")
                        # check if new Tower is active Tower
                        if index == model.activeTowerIndex:
                            # print("same Tower")
                            continue
                        # check if there is already an connection
                        if model.activeTowerIndex in model.towerGraph.connections[index]:
                            # print("already connected")
                            continue

                        # remove old connection
                        model.towerGraph.removeConnectionOfBoostTower(model.activeTowerIndex)

                        # build new Connection and animation
                        model.towerGraph.addConnection(index, model.activeTowerIndex)
                        model.effects.append(
                            AnimationOnce(newTower.rect.centerx, newTower.rect.centery, animBoost4, 10, -90))
                        model.activeTowerIndex = index
                        model.activeTower = newTower
                        soundPowerUp.play()
                        # print("New Tower boosted")
                        break

        model.pressOnBoost = False

    # create towers by left click delete by right
    if input.mouseLeftPressed:

        towerKey = model.towerMenu.getTowerKey(input.cursor)
        if towerKey is not None:
            model.towerListKey = towerKey
            soundSelect1.play()
        if gameArea.collidepoint(input.cursor):
            (x, y) = input.cursor
            cx = x // model.gridSize
            cy = y // model.gridSize
            ct = getCell(cx, cy, model.gridWidth, model.grid)

            # set Tower
            if ct == CellType.FOUNDATION:
                # create Tower
                if model.towerListKey is not None:

                    (spr, agro, time, isBoost, projType, boostType, icon) = towerList[model.towerListKey]

                    pInfo = None
                    if projType is not None:
                        pInfo = projectileList[projType]

                    model.towers.append(
                        Tower((cx + 0.5) * model.gridSize, (cy + 0.5) * model.gridSize, icon, agro, time, isBoost,
                              pInfo,
                              boostType))
                    model.towerGraph.addTower()
                    soundTower.play()
                    model.activeTower = model.towers[-1]
                    model.activeTowerIndex = len(model.towers) - 1
                    # handle Pressing
                    model.pressOnBoost = isBoost
                    model.lastPressPosition = input.cursor
                    model.towerListKey = None
                    model.towerMenu.removeActiveItem()
                    setCell(cx, cy, model.gridWidth, model.grid, CellType.OCCUPIED)
                    # print("create new Tower " + str(isBoost))
                    # set neighbouring cells to foundation
                    if cx >= 2:
                        if getCell(cx - 2, cy, model.gridWidth, model.grid) == CellType.FREE:
                            setCell(cx - 2, cy, model.gridWidth, model.grid, CellType.FOUNDATION)
                    if cx <= model.gridWidth - 3:
                        if getCell(cx + 2, cy, model.gridWidth, model.grid) == CellType.FREE:
                            setCell(cx + 2, cy, model.gridWidth, model.grid, CellType.FOUNDATION)

                    if not isBoost:
                        if cy >= 3:
                            if getCell(cx, cy - 2, model.gridWidth, model.grid) == CellType.FREE:
                                setCell(cx, cy - 2, model.gridWidth, model.grid, CellType.FOUNDATION)
                        if cy <= model.gridHeight - 3:
                            if getCell(cx, cy + 2, model.gridWidth, model.grid) == CellType.FREE:
                                setCell(cx, cy + 2, model.gridWidth, model.grid, CellType.FOUNDATION)

            elif ct == CellType.OCCUPIED:
                for index, t in enumerate(model.towers):
                    if t.rect.collidepoint(input.cursor):
                        model.activeTower = t
                        model.activeTowerIndex = index
                        if t.isBoostTower:
                            model.pressOnBoost = True
                            model.lastPressPosition = input.cursor

            elif ct == CellType.CITY:
                model.activeTower = None
                model.activeTowerIndex = None
            elif ct == CellType.FREE:
                model.activeTower = None
                model.activeTowerIndex = None

                # delete Towers
                # if input.mouseRightPressed:
    # model.towers = list(filter(lambda x: not x.rect.collidepoint(input.cursor), model.towers))

    # if input.numberPressed :
    #    model.towerListIndex = input.numberKey - 1


    # Logic

    # lose condition
    if model.city.health <= 0:
        model.gameState = GameState.RESTART

    # spawn enemy
    '''
    if input.timer % model.spawnrate == 0 or input.timer == 1:
        model.enemiesCreated += 1

        en = Enemy(randint(0,6)*model.gridSize + 32, 0, 1,1,20)

        en.vy = en.speed
        model.enemies.append(en)
    '''

    # new tower in menu
    model.towerSpawnTimer += 1
    if model.towerSpawnTimer == model.towerSpawnRate:
        model.towerMenu.addRandomItem(allTowerTypes)
        model.towerSpawnTimer = 0

    model.enemies = model.enemies + spawnEnemies(model.level, input.timer)

    moveEnemies(model.enemies, model.city, model.towers)
    enemies = model.enemies
    tower, projectiles, num_arrows = shootArrows(model.towerGraph, model.towers, enemies, model.projectiles)
    projectiles, enemies, numHits = collisionArrowsEnemies(projectiles, enemies)

    if numHits > 0:
        soundHit2.play()

    # if num_arrows > 0:
    # shoot_sound.play()
    enemies, city, numAttacks = attackCity(enemies, model.city)

    # update attacks

    for at in range(numAttacks):
        ax = model.city.rect.centerx + randint(-20, 20)  # city.rect.centerx
        ay = model.city.rect.centery + randint(-20, 20)  # city.rect.centery
        model.effects.append(AnimationOnce(ax, ay, [spriteAttack], 50))
        soundHit.play()

    model.projectiles = clearProjectiles(projectiles, model.screenWidth, model.screenHeight)
    model.enemies, deadEnemies = clearEnemies(enemies, model.screenWidth, model.screenHeight)
    for d in deadEnemies:
        model.effects.append(AnimationOnce(d.rect.centerx, d.rect.centery, animExplosion1, 10))

    if deadEnemies:
        model.enemiesKilled += len(deadEnemies)
        model.towerSpawnTimer += len(deadEnemies) * 5
        soundExplosion1.play()

    model.effects = list(filter(lambda x: x.done == False, model.effects))

    sg = RenderPlain(model.groundSprites)

    st = RenderPlain(model.towers)
    st.update()
    se = RenderPlain(model.enemies)
    se.update()
    sa = RenderPlain(model.projectiles)
    sa.update()
    sc = RenderPlain(model.city)

    sef = RenderPlain(model.effects)
    sef.update()

    # Redisplay

    screen.fill((255, 255, 255))

    sg.draw(screen)  # ground
    sc.draw(screen)  # city
    st.draw(screen)  # tower
    se.draw(screen)  # enemy
    sa.draw(screen)  # projectiles
    sef.draw(screen)  # effects

    # draw tower spawntimer
    for index, c in enumerate(model.towerGraph.connections):
        p1 = model.towers[index].rect.center
        for t in c:
            p2 = model.towers[t].rect.center
            pygame.draw.line(screen, (255, 255, 255), p1, p2, 4)

    tstx = 448
    tsty = 64 * len(model.towerMenu.items)

    pygame.draw.rect(screen, (0, 230, 0), (tstx, tsty, 64, model.towerSpawnTimer / model.towerSpawnRate * 64))

    # draw life bar of city

    lfbx = 128
    lfby = 660
    lfblen = 3 * 64
    lfbv = (model.level.city.health / model.level.city.maxHealth ) * lfblen

    pygame.draw.rect(screen, (0, 200, 0), (lfbx, lfby, lfbv, 15))

    if model.pressOnBoost:
        (cx, cy) = input.cursor
        (ax, ay) = model.activeTower.rect.center
        tx = ax - cx
        ty = ay - cy
        if lenVector(tx, ty) < model.boostRange:
            pygame.draw.line(screen, (255, 255, 255), (ax, ay), (cx, cy), 4)

            # draw activeTower
            # if model.activeTower :
            #     pygame.draw.rect(screen, (255,255,255), (model.activeTower.rect))
            #     if model.activeTower.boostTarget :
            #         pygame.draw.rect(screen, (0, 255, 0), (model.activeTower.boostTarget.rect))

    # draw grid
    gridcolor = (20, 20, 20)
    gridsize = 64
    for x in range(8):
        pygame.draw.line(screen, gridcolor, [x * gridsize, 0], [x * gridsize, 11 * gridsize], 1)
    for y in range(12):
        pygame.draw.line(screen, gridcolor, [0, y * gridsize], [7 * gridsize, y * gridsize], 1)

    # draw foundations
    for x in range(7):
        for y in range(11):
            if getCell(x, y, model.gridWidth, model.grid) == CellType.FOUNDATION:
                imgrect = model.foundationImage.get_rect()
                imgrect.topleft = x * model.gridSize, y * model.gridSize
                screen.blit(model.foundationImage, imgrect)

    # draw TowerMenu
    model.towerMenu.draw(screen)

    pygame.display.flip()
