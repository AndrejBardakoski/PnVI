# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys
import time

from pygame.locals import *

FPS = 15
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
BGCOLOR = BLACK

# Change for requirement 1:
ENEMY_WORM_APPEARING_TIME = 20  # the enemy worm will appear 20 seconds after the game starts
ENEMY_WORM_COLOR = (255, 0, 255)  # enemy worm will be purple

# Change for requirement 2:
GOLD_COLOR = (255, 215, 0)
GOLD_APPLE_TIMEOUT = 5  # the golden apple will last for 5s
GOLD_APPLE_COOLDOWN = 5  # the golden apple will reappear in 5s
BLUE = (0, 0, 255)
BLUE_APPLE_TIMEOUT = 7  # the blue apple will last for 7s
BLUE_APPLE_COOLDOWN = 15  # the blue apple will reappear in 15s

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0  # syntactic sugar: index of the worm's head


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


def runGame():
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [{'x': startx, 'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT

    # Change for requirement 1:
    start_time = time.time()  # save the start time
    enemyWormCoords = None  # no enemy worm at the beggining of the game
    playerHitsEnemy = False  # a flag that is true if the player have hit the enemy this turn (frame)
    enemyHitsPlayer = False  # a flah that is true if the enemy has hit the player this turn (frame)
    enemyDirection = RIGHT  # represent the direction of the enemy worm

    # Change for requirement 2:
    golden_apple = getRandomLocation()  # make golden apple at the start of the game
    golden_apple_appearing_time = time.time()  # save the golden apple appearing time
    blue_apple = getRandomLocation()  # make blue apple at the start of the game
    blue_apple_appearing_time = time.time()  # save the blue apple appearing time

    player_score = 0  # player score is 0 at the start of the game
    enemy_score = 0  # enemy score is 0 at the start of the game

    # Start the apple in a random place.
    apple = getRandomLocation()

    while True:  # main game loop
        # Change for requirement 1:
        if enemyWormCoords is None and time.time() - ENEMY_WORM_APPEARING_TIME > start_time:  # if true it is time to create enemy worm
            startx = random.randint(5, CELLWIDTH - 6)
            starty = random.randint(5, CELLHEIGHT - 6)
            enemyWormCoords = [{'x': startx, 'y': starty},
                               {'x': startx - 1, 'y': starty},
                               {'x': startx - 2, 'y': starty}]
        if enemyWormCoords:
            enemyDirection = getRandomDirection(enemyDirection, enemyWormCoords)  # get enemy direction

        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or \
                wormCoords[HEAD]['y'] == CELLHEIGHT:
            return  # game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return  # game over

        # Change for requirement 2:
        if golden_apple is None:
            if time.time() - GOLD_APPLE_COOLDOWN > golden_apple_appearing_time:  # check if golden apple should appear
                golden_apple = getRandomLocation()
                golden_apple_appearing_time = time.time()
        elif time.time() - GOLD_APPLE_TIMEOUT > golden_apple_appearing_time:  # check if golden apple should disappear
            golden_apple = None

        if blue_apple is None:
            if time.time() - BLUE_APPLE_COOLDOWN > blue_apple_appearing_time:  # check if blue apple should appear
                blue_apple = getRandomLocation()
                blue_apple_appearing_time = time.time()
        elif time.time() - BLUE_APPLE_TIMEOUT > blue_apple_appearing_time:  # check if blue apple should disappear
            blue_apple = None

        # Change for requirement 1:
        if enemyWormCoords:  # logic for the enemy worm
            for enemyWormBody in enemyWormCoords:  # check if the player worm has hit the enemy worm
                if coalision(wormCoords[HEAD], enemyWormBody):
                    # if wormCoords[HEAD]['x'] == enemyWormBody['x'] and wormCoords[HEAD]['y'] == enemyWormBody['y']:
                    playerHitsEnemy = True

            for wormBody in wormCoords:  # check if the enemy worm has hit the player worm
                if coalision(enemyWormCoords[HEAD], wormBody):
                    # if enemyWormCoords[HEAD]['x'] == wormBody['x'] and enemyWormCoords[HEAD]['y'] == wormBody['y']:
                    enemyHitsPlayer = True

            # Change for requirement 2:
            if golden_apple and wormEatApple(enemyWormCoords[HEAD], golden_apple):  # check if enemy ate golden apple
                golden_apple = None  # golden_apple is eaten
                enemy_score += 3  # enemy_score increases when enemy eats golden apple
            if blue_apple and wormEatApple(enemyWormCoords[HEAD], blue_apple):  # check if enemy ate blue apple
                blue_apple = None  # blue apple is eaten
                enemy_score += 3  # enemy_score increases when enemy eats blue apple

            if wormEatApple(enemyWormCoords[HEAD], apple):  # check if enemy ate red apple
                apple = getRandomLocation()  # set a new apple somewhere
                enemy_score += 1  # enemy_score increases when enemy eats red apple
            elif playerHitsEnemy:  # check if player hit enemy
                playerHitsEnemy = False  # reset the flag
                enemy_score += 2  # enemy_score increases when player hits enemy
            else:  # if the enemy worm didn't ate apple and didn't got hit by the player
                del enemyWormCoords[-1]  # remove enemy worm's tail segment

        # Change for requirement 2:
        if golden_apple and wormEatApple(wormCoords[HEAD], golden_apple):  # check if player ate golden apple
            golden_apple = None  # golden_apple is eaten
            player_score += 3  # player_score increases when player eats blue apple
        if blue_apple and wormEatApple(wormCoords[HEAD], blue_apple):  # check if player ate blue apple
            blue_apple = None  # blue_apple is eaten
            player_score += 3  # player_score increases when player eats blue apple

        if wormEatApple(wormCoords[HEAD], apple):  # check if player ate red apple
            # if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation()  # set a new apple somewhere
            player_score += 1  # player_score increases when player eats red apple
        # Change for requirement 1:
        elif enemyHitsPlayer:  # check if enemy hit player
            enemyHitsPlayer = False  # reset the flag
            # note: the player don't get additional score for getting hit my the enemy
        else:  # if the player didn't ate apple and didn't got hit by the enemy
            del wormCoords[-1]  # remove worm's tail segment

        # move the worm by adding a segment in the direction it is moving
        # Change for requirement 1:

        # if direction == UP:
        #     newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        # elif direction == DOWN:
        #     newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        # elif direction == LEFT:
        #     newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        # elif direction == RIGHT:
        #     newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
        newHead = getNewHead(wormCoords[HEAD], direction)  # the if else segment is replaced with a function
        wormCoords.insert(0, newHead)  # add the new head to the player worm

        # Change for requirement 1:
        if enemyWormCoords:
            newEnemyHead = getNewHead(enemyWormCoords[HEAD], enemyDirection)  # get new head
            enemyWormCoords.insert(0, newEnemyHead)  # add the new head to the enemy worm

        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        # Change for requirement 1:
        if enemyWormCoords:
            drawWorm(enemyWormCoords, ENEMY_WORM_COLOR)  # draw the enemy worm with its color

        drawApple(apple)
        # Change for requirement 2:
        flashIsOn = round(time.time(), 1) * 10 % 10 >= 2
        # each second the apples will be displayed for 0.7s and not displayed for 0.3s
        if golden_apple and flashIsOn:
            drawApple(golden_apple, GOLD_COLOR)  # drw the golden apple
        flashIsOn = round(time.time(), 1) * 10 % 10 <= 6
        if blue_apple and flashIsOn:
            drawApple(blue_apple, BLUE)  # drw the blue apple

        # Change for requirement 2:
        # drawScore(len(wormCoords) - 3)
        drawScore((player_score - enemy_score) * 100)
        # the total score is calculated as the difference between player score and enemy score, multiplied by 100

        pygame.display.update()
        FPSCLOCK.tick(FPS)


# Change for requirement 1:
# return a random direction for the enemy worm
# there is more chance the direction the worm is currently moving to be returned
# the enemy never hits the screen borders
# the enemy will only eat himself if it has no other options
def getRandomDirection(currentDirection, wormCord):
    head = wormCord[HEAD]
    directions = [LEFT, RIGHT, UP, DOWN]
    # replace the opposite direction with the current
    # the effect of the replacement is removed illegal move and added more chance for the worm to not change direction
    if currentDirection == LEFT:
        directions = [LEFT, LEFT, UP, DOWN]
    if currentDirection == RIGHT:
        directions = [RIGHT, RIGHT, UP, DOWN]
    if currentDirection == UP:
        directions = [LEFT, RIGHT, UP, UP]
    if currentDirection == DOWN:
        directions = [LEFT, RIGHT, DOWN, DOWN]

    # remove the directions from the list that can cause the enemy worm to hit the window border
    if head['x'] == 0:
        while LEFT in directions:
            directions.remove(LEFT)
    if head['x'] == CELLWIDTH - 1:
        while RIGHT in directions:
            directions.remove(RIGHT)
    if head['y'] == 0:
        while UP in directions:
            directions.remove(UP)
    if head['y'] == CELLHEIGHT - 1:
        while DOWN in directions:
            directions.remove(DOWN)
    # make a back-up of the directions list. At this point the list contains at least 1 direction
    backup_directions = directions.copy()

    # get all possible next heads
    head_right = getNewHead(head, RIGHT)
    head_left = getNewHead(head, LEFT)
    head_up = getNewHead(head, UP)
    head_down = getNewHead(head, DOWN)

    # remove the directions from the list that can cause the enemy worm to hit itself
    # after this logic the directions list can be empty
    for body in wormCord:
        if coalision(head_right, body):
            while RIGHT in directions:
                directions.remove(RIGHT)
        elif coalision(head_left, body):
            while LEFT in directions:
                directions.remove(LEFT)
        elif coalision(head_up, body):
            while UP in directions:
                directions.remove(UP)
        elif coalision(head_down, body):
            while DOWN in directions:
                directions.remove(DOWN)

    # return a random direction
    if len(directions) != 0:
        return random.choice(directions)
    return random.choice(backup_directions)


# Change for requirement 1:
# return true if the worm's head is on the same spot as the apple
def wormEatApple(head, apple):
    return coalision(head, apple)


# Change for requirement 1:
# return true if both objects are on the same spot
def coalision(obj1, obj2):
    return obj1['x'] == obj2['x'] and obj1['y'] == obj2['y']


# Change for requirement 1:
# return new head created form the coordinates of the current head moved by one position in the given direction
def getNewHead(head, direction):
    if direction == UP:
        newHead = {'x': head['x'], 'y': head['y'] - 1}
    elif direction == DOWN:
        newHead = {'x': head['x'], 'y': head['y'] + 1}
    elif direction == LEFT:
        newHead = {'x': head['x'] - 1, 'y': head['y']}
    else:  # direction == RIGHT
        newHead = {'x': head['x'] + 1, 'y': head['y']}
    return newHead


def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Wormy!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Wormy!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3  # rotate by 3 degrees each frame
        degrees2 += 7  # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


# Change for requirement 3:
def showGameOverScreen():
    # gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    # gameSurf = gameOverFont.render('Game', True, WHITE)
    # overSurf = gameOverFont.render('Over', True, WHITE)
    # gameRect = gameSurf.get_rect()
    # overRect = overSurf.get_rect()
    # gameRect.midtop = (WINDOWWIDTH / 2, 10)
    # overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    # DISPLAYSURF.blit(gameSurf, gameRect)
    # DISPLAYSURF.blit(overSurf, overRect)
    # drawPressKeyMsg()
    # pygame.display.update()
    # pygame.time.wait(500)
    # checkForKeyPress()  # clear out any key presses in the event queue
    #
    # while True:
    #     if checkForKeyPress():
    #         pygame.event.get()  # clear event queue
    #         return

    # the gameOverFont decreased, game and over surf combined into one gameOver surf
    gameOverFont = pygame.font.Font('freesansbold.ttf', 100)
    gameOverSurf = gameOverFont.render('Game Over', True, WHITE)
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.midtop = (WINDOWWIDTH / 2, 10)

    # added startAgain surf that represent a start again button
    buttonsFont = pygame.font.Font('freesansbold.ttf', 30)
    startAgainSurf = buttonsFont.render('Start from beggining', True, WHITE)
    startAgainRect = startAgainSurf.get_rect()
    startAgainRect.topleft = (30, WINDOWHEIGHT / 2 + 50)

    # added quit surf that represent a quit button
    quitSurf = buttonsFont.render('Quit', True, WHITE)
    quitRect = quitSurf.get_rect()
    quitRect.topright = (WINDOWWIDTH - 100, WINDOWHEIGHT / 2 + 50)

    DISPLAYSURF.blit(gameOverSurf, gameOverRect)
    DISPLAYSURF.blit(startAgainSurf, startAgainRect)
    DISPLAYSURF.blit(quitSurf, quitRect)

    pygame.display.update()
    checkForKeyPress()  # clear out any key presses in the event queue

    while True:
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()
            if event.type == MOUSEBUTTONUP:
                if startAgainRect.collidepoint(event.pos):  # check if start again is clicked
                    return  # this is followed up by runGame()
                elif quitRect.collidepoint(event.pos):  # check if quit is clicked
                    terminate()  # quit the game


def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


# Change for requirement 1:
# the function is changed so it can draw a worm in a color passed as an argument
# def drawWorm(wormCoords):
def drawWorm(wormCoords, color=GREEN):
    # Change for requirement 1:
    r, g, b = color
    dark_color = (int(r * 0.75), int(g * 0.75), int(b * 0.75))  # get a dark variant of the color, used for 3D effect
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        # Change for requirement 1:
        # pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        pygame.draw.rect(DISPLAYSURF, dark_color, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        # pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)
        pygame.draw.rect(DISPLAYSURF, color, wormInnerSegmentRect)


# Change for requirement 2:
# the function is changed so it can draw an apple in a color passed as an argument
# def drawApple(coord):
def drawApple(coord, color=RED):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    # Change for requirement 2:
    # pygame.draw.rect(DISPLAYSURF, RED, appleRect)
    pygame.draw.rect(DISPLAYSURF, color, appleRect)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):  # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):  # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()
