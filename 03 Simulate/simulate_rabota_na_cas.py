# Simulate (a Simon clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, sys, time, pygame
from pygame.locals import *

FPS = 30
# CHANGE for request 5 and 6
# WINDOWWIDTH = 640
# WINDOWHEIGHT = 480
WINDOWWIDTH = 960
WINDOWHEIGHT = 720

FLASHSPEED = 500  # in milliseconds
FLASHDELAY = 200  # in milliseconds
# CHANGE for request 6
# BUTTONSIZE = 200
# BUTTONGAPSIZE = 20
BUTTONSIZE = 260
BUTTONGAPSIZE = 30

# TIMEOUT = 4 # seconds before game over if no button is pushed.

#                R    G    B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# BRIGHTRED = (255, 0, 0)
# RED = (155, 0, 0)
# BRIGHTGREEN = (0, 255, 0)
# GREEN = (0, 155, 0)
# BRIGHTBLUE = (0, 0, 255)
# BLUE = (0, 0, 155)
# BRIGHTYELLOW = (255, 255, 0)
# YELLOW = (155, 155, 0)
DARKGRAY = (40, 40, 40)
bgColor = BLACK

# CHANGE for request 4
BRIGHTRED = (255, 20, 30)
RED = (170, 10, 15)
BRIGHTGREEN = (20, 255, 40)
GREEN = (10, 160, 20)
BRIGHTBLUE = (20, 20, 255)
BLUE = (10, 10, 135)
BRIGHTYELLOW = (255, 255, 10)
YELLOW = (120, 120, 5)

# CHANGE for request 5
BRIGHTPINK = (255, 0, 255)
PINK = (150, 0, 150)
BRIGHTCYAN = (0, 255, 255)
CYAN = (0, 140, 140)

# CHANGE for request 5
# XMARGIN = int((WINDOWWIDTH - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)
XMARGIN = int((WINDOWWIDTH - (3 * BUTTONSIZE) - 2 * BUTTONGAPSIZE) / 2)

YMARGIN = int((WINDOWHEIGHT - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)

# Rect objects for each of the four buttons
YELLOWRECT = pygame.Rect(XMARGIN, YMARGIN, BUTTONSIZE, BUTTONSIZE)
BLUERECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN, BUTTONSIZE, BUTTONSIZE)
REDRECT = pygame.Rect(XMARGIN, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
GREENRECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE,
                        BUTTONSIZE)
# CHANGE for request 5

PINKRECT = pygame.Rect(XMARGIN + 2 * BUTTONSIZE + 2 * BUTTONGAPSIZE, YMARGIN, BUTTONSIZE, BUTTONSIZE)
CYANRECT = pygame.Rect(XMARGIN + 2 * BUTTONSIZE + 2 * BUTTONGAPSIZE, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE,
                       BUTTONSIZE)


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BEEP1, BEEP2, BEEP3, BEEP4

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Simulate')

    BASICFONT = pygame.font.Font('freesansbold.ttf', 16)
    infoSurf = BASICFONT.render('Match the pattern by clicking on the button or using the Q, W, A, S keys.', 1,
                                DARKGRAY)
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (10, WINDOWHEIGHT - 25)

    # load the sound files
    BEEP1 = pygame.mixer.Sound('beep1.ogg')
    BEEP2 = pygame.mixer.Sound('beep2.ogg')
    BEEP3 = pygame.mixer.Sound('beep3.ogg')
    BEEP4 = pygame.mixer.Sound('beep4.ogg')

    # Initialize some variables for a new game
    pattern = []  # stores the pattern of colors
    currentStep = 0  # the color the player must push next
    lastClickTime = 0  # timestamp of the player's last button push
    score = 0
    # CHANGE for request 9
    highscore = 0
    # CHANGE for request 1
    TIMEOUT = 5  # starts from 5sec

    # when False, the pattern is playing. when True, waiting for the player to click a colored button:
    waitingForInput = False

    while True:  # main game loop
        clickedButton = None  # button that was clicked (set to YELLOW, RED, GREEN, or BLUE)
        DISPLAYSURF.fill(bgColor)
        drawButtons()

        scoreSurf = BASICFONT.render('Score: ' + str(score), 1, WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINDOWWIDTH - 100, 10)
        DISPLAYSURF.blit(scoreSurf, scoreRect)

        # CHANGE for request 9
        highscoreSurf = BASICFONT.render('HighScore: ' + str(highscore), 1, WHITE)
        highscoreRect = highscoreSurf.get_rect()
        highscoreRect.topleft = (WINDOWWIDTH - 135, 30)
        DISPLAYSURF.blit(highscoreSurf, highscoreRect)

        DISPLAYSURF.blit(infoSurf, infoRect)

        checkForQuit()
        for event in pygame.event.get():  # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                clickedButton = getButtonClicked(mousex, mousey)
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    clickedButton = YELLOW
                elif event.key == K_w:
                    clickedButton = BLUE
                elif event.key == K_a:
                    clickedButton = RED
                elif event.key == K_s:
                    clickedButton = GREEN
                # CHANGE for request 5
                elif event.key == K_e:
                    clickedButton = PINK
                elif event.key == K_d:
                    clickedButton = CYAN

        if not waitingForInput:
            # play the pattern
            pygame.display.update()
            pygame.time.wait(1000)
            # CHANGE for request 2
            # pattern.append(random.choice((YELLOW, BLUE, RED, GREEN)))
            # CHANGE for request 5
            # pattern.insert(0, (random.choice((YELLOW, BLUE, RED, GREEN))))  # Insert at the start of the pattern
            pattern.insert(0, (random.choice((YELLOW, BLUE, RED, GREEN, PINK, CYAN))))

            for button in pattern:
                flashButtonAnimation(button)
                pygame.time.wait(FLASHDELAY)
            waitingForInput = True
        else:
            # wait for the player to enter buttons
            if clickedButton and clickedButton == pattern[currentStep]:
                # pushed the correct button
                flashButtonAnimation(clickedButton)
                currentStep += 1
                lastClickTime = time.time()

                if currentStep == len(pattern):
                    # pushed the last button in the pattern
                    changeBackgroundAnimation()
                    score += 1
                    # CHANGE  for request 9
                    if score >= highscore:
                        highscore = score

                    waitingForInput = False
                    currentStep = 0  # reset back to first step
                    # CHANGE  for request 1
                    if len(pattern) % 7 == 0 and TIMEOUT > 1:
                        TIMEOUT -= 1

            elif (clickedButton and clickedButton != pattern[currentStep]) or (
                    currentStep != 0 and time.time() - TIMEOUT > lastClickTime):
                # pushed the incorrect button, or has timed out
                gameOverAnimation()
                # reset the variables for a new game:
                pattern = []
                currentStep = 0
                waitingForInput = False
                score = 0
                # CHANGE for request 1
                TIMEOUT = 5  # starts from 5sec

                pygame.time.wait(1000)
                changeBackgroundAnimation()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT):  # get all the QUIT events
        terminate()  # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP):  # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate()  # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event)  # put the other KEYUP event objects back


def flashButtonAnimation(color, animationSpeed=50):
    if color == YELLOW:
        sound = BEEP1
        flashColor = BRIGHTYELLOW
        rectangle = YELLOWRECT
    elif color == BLUE:
        sound = BEEP2
        flashColor = BRIGHTBLUE
        rectangle = BLUERECT
    elif color == RED:
        sound = BEEP3
        flashColor = BRIGHTRED
        rectangle = REDRECT
    elif color == GREEN:
        sound = BEEP4
        flashColor = BRIGHTGREEN
        rectangle = GREENRECT
    # CHANGE for request 5
    elif color == PINK:
        sound = BEEP2
        flashColor = BRIGHTPINK
        rectangle = PINKRECT
    elif color == CYAN:
        sound = BEEP1
        flashColor = BRIGHTCYAN
        rectangle = CYANRECT

    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface((BUTTONSIZE, BUTTONSIZE))
    flashSurf = flashSurf.convert_alpha()
    r, g, b = flashColor
    sound.play()
    for start, end, step in ((0, 255, 1), (255, 0, -1)):  # animation loop
        for alpha in range(start, end, animationSpeed * step):
            checkForQuit()
            DISPLAYSURF.blit(origSurf, (0, 0))
            flashSurf.fill((r, g, b, alpha))
            DISPLAYSURF.blit(flashSurf, rectangle.topleft)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
    DISPLAYSURF.blit(origSurf, (0, 0))


def drawButtons():
    pygame.draw.rect(DISPLAYSURF, YELLOW, YELLOWRECT)
    pygame.draw.rect(DISPLAYSURF, BLUE, BLUERECT)
    pygame.draw.rect(DISPLAYSURF, RED, REDRECT)
    pygame.draw.rect(DISPLAYSURF, GREEN, GREENRECT)
    # CHANGE for request 5
    pygame.draw.rect(DISPLAYSURF, PINK, PINKRECT)
    pygame.draw.rect(DISPLAYSURF, CYAN, CYANRECT)


def changeBackgroundAnimation(animationSpeed=40):
    global bgColor
    newBgColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    newBgSurf = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
    newBgSurf = newBgSurf.convert_alpha()
    r, g, b = newBgColor
    for alpha in range(0, 255, animationSpeed):  # animation loop
        checkForQuit()
        DISPLAYSURF.fill(bgColor)

        newBgSurf.fill((r, g, b, alpha))
        DISPLAYSURF.blit(newBgSurf, (0, 0))

        drawButtons()  # redraw the buttons on top of the tint

        pygame.display.update()
        FPSCLOCK.tick(FPS)
    bgColor = newBgColor


def gameOverAnimation(color=WHITE, animationSpeed=50):
    # play all beeps at once, then flash the background
    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface(DISPLAYSURF.get_size())
    flashSurf = flashSurf.convert_alpha()
    BEEP1.play()  # play all four beeps at the same time, roughly.
    BEEP2.play()
    BEEP3.play()
    BEEP4.play()
    r, g, b = color
    # CHANGE for request 3
    # for i in range(3):  # do the flash 3 times
    for i in range(5):  # Now we will do the flash 5 times

        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            # The first iteration in this loop sets the following for loop
            # to go from 0 to 255, the second from 255 to 0.
            for alpha in range(start, end, animationSpeed * step):  # animation loop
                # alpha means transparency. 255 is opaque, 0 is invisible
                checkForQuit()
                flashSurf.fill((r, g, b, alpha))
                DISPLAYSURF.blit(origSurf, (0, 0))
                DISPLAYSURF.blit(flashSurf, (0, 0))
                drawButtons()
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def getButtonClicked(x, y):
    if YELLOWRECT.collidepoint((x, y)):
        return YELLOW
    elif BLUERECT.collidepoint((x, y)):
        return BLUE
    elif REDRECT.collidepoint((x, y)):
        return RED
    elif GREENRECT.collidepoint((x, y)):
        return GREEN
    # CHANGE for request 5
    elif PINKRECT.collidepoint((x, y)):
        return PINK
    elif CYANRECT.collidepoint((x, y)):
        return CYAN
    return None


if __name__ == '__main__':
    main()
