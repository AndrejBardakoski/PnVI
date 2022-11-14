# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys
import time

from pygame.locals import *

# Change for requirement 4:
# FPS = 15
FPS_INCREMENT = 3
FPS_INTERVAL = 30

# Change for requirement 2:
# WINDOWWIDTH = 640
# WINDOWHEIGHT = 480
WINDOWWIDTH = 800
WINDOWHEIGHT = 600

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

# Change for requirement 7:
OBSTACLE_COLOR = (133, 127, 40)
OBSTACLE_INER_COLOR = (179, 170, 39)
NUM_OBSTACLES = int(CELLHEIGHT * CELLWIDTH * 0.02)  # 2% of the board will be obstacles

# Change for requirement 3:
GOLD_COLOR = (255, 215, 0)
GOLD_APPLE_TIMEOUT = 5  # the golden apple will last for 5s
GOLD_APPLE_COOLDOWN = 15  # the golden apple will reappear in 15s

# Change for requirement 5:
BLUE = (0, 0, 255)
BLUE_APPLE_TIMEOUT = 3  # the blue apple will last for 3s
BLUE_APPLE_COOLDOWN = 25  # the golden apple will reappear in 25s

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0  # syntactic sugar: index of the worm's head


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    # Change for requirement 4:
    global FPS
    FPS = 7

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')

    showStartScreen()
    while True:
        # Change for requirement 4:
        FPS = 7

        runGame()
        showGameOverScreen()


def runGame():
    # Change for requirement 4:
    global FPS
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [{'x': startx, 'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT

    # Change for requirement 7:
    obstacles = get_obstacles()

    # Start the apple in a random place.
    apple = getRandomLocation(obstacles)
    # Change for requirement 3:
    golden_apple = getRandomLocation(obstacles)
    golden_apple_appearing_time = time.time()
    # Change for requirement 5:
    blue_apple = getRandomLocation(obstacles)
    blue_apple_appearing_time = time.time()
    # Change for requirement 4:
    speed_up_timestamp = time.time()
    # Change for requirement 6:
    worm_color = DARKGREEN

    while True:  # main game loop
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
        # Change for requirement 4:
        if time.time() - FPS_INTERVAL > speed_up_timestamp:
            FPS += FPS_INCREMENT
            speed_up_timestamp = time.time()
            # Change for requirement 6:
            worm_color = getRandomColor()
        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or \
                wormCoords[HEAD]['y'] == CELLHEIGHT:
            return  # game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return  # game over

        # Change for requirement 7:
        for obstacle in obstacles:
            if wormCoords[HEAD]['x'] == obstacle['x'] and wormCoords[HEAD]['y'] == obstacle['y']:
                return  # game over

        # check if worm has eaten an apply
        # Change for requirement 3:
        if golden_apple is None:
            if time.time() - GOLD_APPLE_COOLDOWN > golden_apple_appearing_time:
                golden_apple = getRandomLocation(obstacles)
                golden_apple_appearing_time = time.time()
        elif time.time() - GOLD_APPLE_TIMEOUT > golden_apple_appearing_time:
            golden_apple = None

        # Change for requirement 5:
        if blue_apple is None:
            if time.time() - BLUE_APPLE_COOLDOWN > blue_apple_appearing_time:
                blue_apple = getRandomLocation(obstacles)
                blue_apple_appearing_time = time.time()
        elif time.time() - BLUE_APPLE_TIMEOUT > blue_apple_appearing_time:
            blue_apple = None

        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation(obstacles)  # set a new apple somewhere
        # Change for requirement 3:
        elif golden_apple and wormCoords[HEAD]['x'] == golden_apple['x'] and wormCoords[HEAD]['y'] == golden_apple['y']:
            golden_apple = None
            if len(wormCoords) > 3:
                del wormCoords[-1]
            del wormCoords[-1]
        # Change for requirement 5:
        elif blue_apple and wormCoords[HEAD]['x'] == blue_apple['x'] and wormCoords[HEAD]['y'] == blue_apple['y']:
            blue_apple = None
            if FPS > 6:
                FPS -= FPS_INCREMENT
                # Change for requirement 6:
                worm_color = getRandomColor()
            del wormCoords[-1]
        else:
            del wormCoords[-1]  # remove worm's tail segment

        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
        wormCoords.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        # Change for requirement 6:
        drawWorm(wormCoords, worm_color)

        drawApple(apple)
        # Change for requirement 3:
        if (golden_apple):
            drawApple(golden_apple, GOLD_COLOR)
        # Change for requirement 5:
        if (blue_apple):
            drawApple(blue_apple, BLUE)
        # Change for requirement 7:
        drawObstacles(obstacles)

        drawScore(len(wormCoords) - 3)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


# Change for requirement 7:
def get_obstacles():
    obstacles = []
    for i in range(NUM_OBSTACLES):
        obstacles.append(getRandomLocation(obstacles))
    return obstacles


# Change for requirement 7:
def drawObstacles(obstacles):
    for obstacle in obstacles:
        x = obstacle['x'] * CELLSIZE
        y = obstacle['y'] * CELLSIZE
        obstacleSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, OBSTACLE_COLOR, obstacleSegmentRect)
        obstacleInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, OBSTACLE_INER_COLOR, obstacleInnerSegmentRect)


# Change for requirement 6:
def getRandomColor():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


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

# Change for requirement 7:
# def getRandomLocation():
def getRandomLocation(obstacles = []):
    tiles = []
    for i in range (CELLWIDTH):
        for j in range (CELLHEIGHT):
            tiles.append({'x': i,'y': j})
            for obstacle in obstacles:
                if obstacle['x']==i and obstacle['y']==j:
                    del tiles[-1]
                    break
    return random.choice(tiles)


def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()  # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return


def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


# Change for requirement 6:
# def drawWorm(wormCoords):
def drawWorm(wormCoords, color=GREEN):
    # Change for requirement 6:
    r, g, b = color
    dark_color = (int(r * 0.75), int(g * 0.75), int(b * 0.75))
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        # Change for requirement 6:
        # pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        pygame.draw.rect(DISPLAYSURF, dark_color, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        # pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)
        pygame.draw.rect(DISPLAYSURF, color, wormInnerSegmentRect)


# Change for requirement 3:
# def drawApple(coord):
def drawApple(coord, color=RED):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    # Change for requirement 3:
    # pygame.draw.rect(DISPLAYSURF, RED, appleRect)
    pygame.draw.rect(DISPLAYSURF, color, appleRect)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):  # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):  # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()
