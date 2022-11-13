import math
import sys

import pygame
from pygame.locals import *
import array

pygame.init()

FPS = 30
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((800, 800), 0, 32)
DISPLAYSURF.fill((0, 0, 0))
pygame.display.set_caption("Let's PLAY")

TWO_PI = math.pi * 2
PI_OVER_3 = TWO_PI / 6

NUM_ANGLES = 128
angle = 0.0
radius = 100
angle_inc = TWO_PI / NUM_ANGLES

color_red = 255
color_green = 0
color_blue = 0
color_inc = 6 * 255 / NUM_ANGLES

vertices = [(0,0)] * 200
colors = [(0,0)] * 200
center = (400, 400)

# for i in range(NUM_ANGLES+1):
#     if angle < PI_OVER_3:
#         color_green += color_inc
#     elif angle < 2 * PI_OVER_3:
#         color_red -= color_inc
#     elif angle < 3 * PI_OVER_3:
#         color_blue += color_inc
#     elif angle < 4 * PI_OVER_3:
#         color_green -= color_inc
#     elif angle < 5 * PI_OVER_3:
#         color_red += color_inc
#     else:
#         color_blue -= color_inc
#     if color_green > 255: color_green = 255
#     if color_green < 0: color_green = 0
#     if color_red > 255: color_red = 255
#     if color_red < 0: color_red = 0
#     if color_blue > 255: color_blue = 255
#     if color_blue < 0: color_blue = 0
#     vertices.append((radius * math.cos(angle)+center[0], radius * math.sin(angle)+center[1]))
#     colors.append((color_red, color_green, color_blue))
#
#     angle += angle_inc

ball_velocity_x = 5
ball_velocity_y = 7

while True:
    DISPLAYSURF.fill((0, 0, 0))
    center = (center[0] + ball_velocity_x, center[1] + ball_velocity_y)
    if center[0] > 700 or center[0] < 100:
        ball_velocity_x *= -1
    if center[1] > 700 or center[1] < 100:
        ball_velocity_y *= -1

    angle = 0.0
    color_red = 255
    color_green = 0
    color_blue = 0
    vertices[0] = (radius * math.cos(angle) + center[0], radius * math.sin(angle) + center[1])

    for i in range(NUM_ANGLES + 1):
        if angle < PI_OVER_3:
            color_green += color_inc
        elif angle < 2 * PI_OVER_3:
            color_red -= color_inc
        elif angle < 3 * PI_OVER_3:
            color_blue += color_inc
        elif angle < 4 * PI_OVER_3:
            color_green -= color_inc
        elif angle < 5 * PI_OVER_3:
            color_red += color_inc
        else:
            color_blue -= color_inc
        if color_green > 255: color_green = 255
        if color_green < 0: color_green = 0
        if color_red > 255: color_red = 255
        if color_red < 0: color_red = 0
        if color_blue > 255: color_blue = 255
        if color_blue < 0: color_blue = 0
        colors[i] = (color_red, color_green, color_blue)
        vertices[i + 1] = (radius * math.cos(angle) + center[0], radius * math.sin(angle) + center[1])

        angle += angle_inc
    for i in range(NUM_ANGLES + 1):
        pygame.draw.polygon(DISPLAYSURF, colors[i], (center, vertices[i], vertices[i + 1]))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    fpsClock.tick(FPS)
