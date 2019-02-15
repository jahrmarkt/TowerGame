# Import ini
from model import *
from update import updateRun

""""
TODO 

"""


def main():
    gameName = "Magic Towers"
    screen.fill((255, 255, 255))
    pygame.display.set_caption(gameName)


    # Text
    font = pygame.font.SysFont("impact", 24)
    font2 = pygame.font.SysFont("impact", 36)
    fontTitle = pygame.font.SysFont("impact", 48)
    scoreColor = (255, 215, 0)  # gold
    menuBgColor = (104, 34, 139)  # indigo

    textHeader1 = fontTitle.render(gameName, True, scoreColor)
    textHeader2 = font2.render("Pause", True, scoreColor)
    textHeader3 = font2.render("You Lost", True, scoreColor)

    textMenu1 = font2.render("Continue?", True, scoreColor)
    textMenu2 = font2.render("Try Again?", True, scoreColor)
    textMenu3 = font2.render("Press Enter", True, scoreColor)
    textMenu4 = font2.render("Start Game?", True, scoreColor)

    textScore = font.render(str(0), True, scoreColor)

    screenHeaderY = height / 4
    (screenMiddleX, screenMiddleY) = (width / 2, height / 2)

    # Assign Key Variables
    keepGoing = True
    clock = pygame.time.Clock()
    timer = 0

    input = Input()
    model = Model(width, height)
    model.gameState = GameState.INTRO

    # Loop
    while keepGoing:
        # Timer
        clock.tick(50)
        timer = timer + 1
        input.reset()  # setze input zurück
        input.timer = timer

        # Input
        for event in pygame.event.get():
            if event.type == QUIT:
                keepGoing = False
                break
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    input.returnKey = True
                elif event.key == K_0:  # numberkeys nur zum testen
                    input.numberPressed = True
                    input.numberKey = 0
                elif event.key == K_1:
                    input.numberPressed = True
                    input.numberKey = 1
                elif event.key == K_2:
                    input.numberPressed = True
                    input.numberKey = 2
                elif event.key == K_3:
                    input.numberPressed = True
                    input.numberKey = 3
                elif event.key == K_4:
                    input.numberPressed = True
                    input.numberKey = 4
                elif event.key == K_5:
                    input.numberPressed = True
                    input.numberKey = 5
                elif event.key == K_6:
                    input.numberPressed = True
                    input.numberKey = 6
                elif event.key == K_7:
                    input.numberPressed = True
                    input.numberKey = 7
                elif event.key == K_8:
                    input.numberPressed = True
                    input.numberKey = 8
                elif event.key == K_9:
                    input.numberPressed = True
                    input.numberKey = 9
            if event.type == MOUSEBUTTONDOWN:
                input.mouseLeftPressed = event.button == 1
                input.mouseRightPressed = event.button == 3
                input.cursor = pygame.mouse.get_pos()
            if event.type == MOUSEBUTTONUP:
                input.mouseLeftReleased = event.button == 1
                input.cursor = pygame.mouse.get_pos()
            if event.type == MOUSEMOTION:
                input.cursor = pygame.mouse.get_pos()

        if model.gameState == GameState.RUN:
            updateRun(input, screen, model)
        elif model.gameState == GameState.INTRO:
            # update
            if input.returnKey:
                model = Model(width, height)
                model.gameState = GameState.RUN

            # Redisplay
            screen.fill(menuBgColor)

            screen.blit(textHeader1,
                        (screenMiddleX - textHeader1.get_width() // 2, screenHeaderY - textHeader1.get_height() // 2))

            screen.blit(textMenu4,
                        (screenMiddleX - textMenu4.get_width() // 2, screenMiddleY - textMenu4.get_height() // 2))
            screen.blit(textMenu3,
                        (screenMiddleX - textMenu3.get_width() // 2, screenMiddleY + 50 - textMenu3.get_height() // 2))
            pygame.display.flip()

        elif model.gameState == GameState.RESTART:
            # update
            if input.returnKey:
                model = Model(width, height)
                model.gameState = GameState.RUN

            # Redisplay
            screen.fill(menuBgColor)

            screen.blit(textHeader3,
                        (screenMiddleX - textHeader3.get_width() // 2, screenHeaderY - textHeader3.get_height() // 2))

            textScore = font.render("Enemies Killed: " + str(model.enemiesKilled), True, scoreColor)
            screen.blit(textScore,
                        (screenMiddleX - textScore.get_width() // 2, screenMiddleY - textScore.get_height() // 2))
            screen.blit(textMenu2,
                        (screenMiddleX - textMenu2.get_width() // 2, screenMiddleY + 50 - textMenu2.get_height() // 2))
            screen.blit(textMenu3,
                        (screenMiddleX - textMenu3.get_width() // 2, screenMiddleY + 100 - textMenu3.get_height() // 2))
            pygame.display.flip()

        elif model.gameState == GameState.PAUSE:
            # update
            if input.returnKey:
                model.gameState = GameState.RUN

            # Redisplay
            screen.fill(menuBgColor)

            # Display text
            screen.blit(textHeader2,
                        (screenMiddleX - textHeader2.get_width() // 2, screenHeaderY - textHeader2.get_height() // 2))
            textScore = font.render("Enemies Killed: " + str(model.enemiesKilled), True, scoreColor)
            screen.blit(textScore,
                        (screenMiddleX - textScore.get_width() // 2, screenMiddleY - textScore.get_height() // 2))
            screen.blit(textMenu1,
                        (screenMiddleX - textMenu1.get_width() // 2, screenMiddleY + 50 - textMenu1.get_height() // 2))
            screen.blit(textMenu3,
                        (screenMiddleX - textMenu3.get_width() // 2, screenMiddleY + 100 - textMenu3.get_height() // 2))

        pygame.display.flip()


main()
