# Simulate (a Simon clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, sys, time, pygame
from pygame.locals import *

FPS = 30
# Change for requirement 3:
# WINDOWWIDTH = 640
# WINDOWHEIGHT = 480
WINDOWWIDTH = 960
WINDOWHEIGHT = 720
# BUTTONSIZE = 200

FLASHSPEED = 500  # in milliseconds
FLASHDELAY = 200  # in milliseconds
BUTTONGAPSIZE = 20
# Change for requirement 2:
# TIMEOUT = 4 # seconds before game over if no button is pushed.


#                R    G    B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BRIGHTRED = (255, 0, 0)
RED = (155, 0, 0)
BRIGHTGREEN = (0, 255, 0)
GREEN = (0, 155, 0)
BRIGHTBLUE = (0, 0, 255)
BLUE = (0, 0, 155)
BRIGHTYELLOW = (255, 255, 0)
YELLOW = (155, 155, 0)
DARKGRAY = (40, 40, 40)
bgColor = BLACK

# Change for requirement 3:
# XMARGIN = int((WINDOWWIDTH - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)
# YMARGIN = int((WINDOWHEIGHT - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)
XMARGIN = 165
YMARGIN = 60


# Rect objects for each of the four buttons
# YELLOWRECT = pygame.Rect(XMARGIN, YMARGIN, BUTTONSIZE, BUTTONSIZE)
# BLUERECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN, BUTTONSIZE, BUTTONSIZE)
# REDRECT = pygame.Rect(XMARGIN, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
# GREENRECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BEEP1, BEEP2, BEEP3, BEEP4
    # Change for requirement 3:
    global buttons

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Simulate')

    BASICFONT = pygame.font.Font('freesansbold.ttf', 16)
    # Change for requirement 3:
    # infoSurf = BASICFONT.render('Match the pattern by clicking on the button or using the Q, W, A, S keys.', 1, DARKGRAY)
    infoSurf = BASICFONT.render('Match the pattern by clicking on the button.', 1, DARKGRAY)

    infoRect = infoSurf.get_rect()
    infoRect.topleft = (10, WINDOWHEIGHT - 25)

    # load the sound files
    BEEP1 = pygame.mixer.Sound('beep1.ogg')
    BEEP2 = pygame.mixer.Sound('beep2.ogg')
    BEEP3 = pygame.mixer.Sound('beep3.ogg')
    BEEP4 = pygame.mixer.Sound('beep4.ogg')

    # Initialize some variables for a new game
    # Change for requirement 3:
    buttons = []
    button_size = getButtonsSize(2)
    for i,j in [(0,0),(0,1),(1,0),(1,1)]:
        buttons.append(createButton(i, j, button_size))

    pattern = []  # stores the pattern of colors
    currentStep = 0  # the color the player must push next
    lastClickTime = 0  # timestamp of the player's last button push
    score = 0
    # Change for requirement 2:
    TIMEOUT = 5  # seconds before game over if no button is pushed.

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

        DISPLAYSURF.blit(infoSurf, infoRect)

        checkForQuit()
        for event in pygame.event.get():  # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                clickedButton = getButtonClicked(mousex, mousey)
            # Change for requirement 3:
            # elif event.type == KEYDOWN:
            #     if event.key == K_q:
            #         clickedButton = YELLOW
            #     elif event.key == K_w:
            #         clickedButton = BLUE
            #     elif event.key == K_a:
            #         clickedButton = RED
            #     elif event.key == K_s:
            #         clickedButton = GREEN

        if not waitingForInput:
            # play the pattern
            pygame.display.update()
            pygame.time.wait(1000)
            # Change for requirement 2 & 3:
            if score % 10 == 0 and score != 0:
                num_buttons_row = int(score / 10) + 2
                button_size = getButtonsSize(num_buttons_row)
                updateButtons(buttons, button_size)
                for i in range(num_buttons_row):
                    buttons.append(createButton(i, num_buttons_row - 1, button_size))
                for i in range(num_buttons_row - 1):
                    buttons.append(createButton(num_buttons_row - 1, i, button_size))
                if TIMEOUT > 3:
                    TIMEOUT -= 1

                DISPLAYSURF.fill(bgColor)
                drawButtons()
            # Change for requirement 1 & 3:
            pattern_len = len(pattern)
            pattern = []
            for i in range(pattern_len):
                pattern.append(random.choice(buttons))
                # pattern.append(random.choice((YELLOW, BLUE, RED, GREEN)))
            pattern.append(random.choice(buttons))
            # pattern.append(random.choice((YELLOW, BLUE, RED, GREEN)))

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
                    waitingForInput = False
                    currentStep = 0  # reset back to first step

            elif (clickedButton and clickedButton != pattern[currentStep]) or (
                    currentStep != 0 and time.time() - TIMEOUT > lastClickTime):
                # pushed the incorrect button, or has timed out
                gameOverAnimation()
                # reset the variables for a new game:
                # Change for requirement 3:
                buttons = []
                button_size = getButtonsSize(2)
                for i, j in [(0, 0), (0, 1), (1, 0), (1, 1)]:
                    buttons.append(createButton(i, j, button_size))

                pattern = []
                currentStep = 0
                waitingForInput = False
                score = 0
                pygame.time.wait(1000)
                changeBackgroundAnimation()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


# Change for requirement 3:
def createButton(xpos, ypos, buttonSize):
    button = {}
    button["xpos"] = xpos
    button["ypos"] = ypos
    button['color'] = (random.randint(20, 170), random.randint(20, 170), random.randint(20, 170))
    button['lightColor'] = (button['color'][0] * 1.5, button['color'][1] * 1.5, button['color'][2] * 1.5)
    button['size'] = buttonSize
    button['rect'] = pygame.Rect(XMARGIN + xpos * buttonSize + (xpos - 1) * BUTTONGAPSIZE,
                                 YMARGIN + ypos * buttonSize + (ypos - 1) * BUTTONGAPSIZE,
                                 buttonSize, buttonSize)
    button['beep'] = random.choice((BEEP1, BEEP2, BEEP3, BEEP4))
    return button


# Change for requirement 3:
def getButtonsSize(numButtonsInRow):
    return int((WINDOWWIDTH - (XMARGIN * 2) - (BUTTONGAPSIZE * numButtonsInRow - 1)) / numButtonsInRow)


# Change for requirement 3:
def updateButtons(buttons, buttonSize):
    for button in buttons:
        button['size'] = buttonSize
        xpos = button["xpos"]
        ypos = button["ypos"]
        button['rect'] = pygame.Rect(XMARGIN + xpos * buttonSize + (xpos - 1) * BUTTONGAPSIZE,
                                     YMARGIN + ypos * buttonSize + (ypos - 1) * BUTTONGAPSIZE,
                                     buttonSize, buttonSize)


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


# Change for requirement 3:
def flashButtonAnimation(button, animationSpeed=50):
    # if color == YELLOW:
    #     sound = BEEP1
    #     flashColor = BRIGHTYELLOW
    #     rectangle = YELLOWRECT
    # elif color == BLUE:
    #     sound = BEEP2
    #     flashColor = BRIGHTBLUE
    #     rectangle = BLUERECT
    # elif color == RED:
    #     sound = BEEP3
    #     flashColor = BRIGHTRED
    #     rectangle = REDRECT
    # elif color == GREEN:
    #     sound = BEEP4
    #     flashColor = BRIGHTGREEN
    #     rectangle = GREENRECT

    sound = button['beep']
    flashColor = button['lightColor']
    rectangle = button['rect']
    buttonSize = button['size']

    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface((buttonSize, buttonSize))
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


# Change for requirement 3:
def drawButtons():
    # pygame.draw.rect(DISPLAYSURF, YELLOW, YELLOWRECT)
    # pygame.draw.rect(DISPLAYSURF, BLUE, BLUERECT)
    # pygame.draw.rect(DISPLAYSURF, RED, REDRECT)
    # pygame.draw.rect(DISPLAYSURF, GREEN, GREENRECT)
    for button in buttons:
        pygame.draw.rect(DISPLAYSURF, button['color'], button['rect'])


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
    for i in range(3):  # do the flash 3 times
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


# Change for requirement 3:
def getButtonClicked(x, y):
    for button in buttons:
        if button['rect'].collidepoint((x, y)):
            return button
    # if YELLOWRECT.collidepoint((x, y)):
    #     return YELLOW
    # elif BLUERECT.collidepoint((x, y)):
    #     return BLUE
    # elif REDRECT.collidepoint((x, y)):
    #     return RED
    # elif GREENRECT.collidepoint((x, y)):
    #     return GREEN
    return None


if __name__ == '__main__':
    main()
