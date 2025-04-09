# IDEA
# Import and Initialize
import pygame
from pygame.locals import *
pygame.init()

# Display configuration
size = (640,480)
screen = pygame.display.set_mode(size)
screen.fill((255,255,255))
pygame.display.set_caption('PaintBrush')

# Entities
brush = pygame.image.load('images/black_brush.png')
brush = pygame.transform.scale(brush, (32,32))
# Action
# ALTER

# VARIABLES
keepGoing = True
paint = False
clock = pygame.time.Clock()


# LOOP
while keepGoing:
    # TIMER
    clock.tick(1000)

    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == QUIT:
            keepGoing = False
            break
        elif event.type == MOUSEBUTTONDOWN:
            paint = True
        elif event.type == MOUSEBUTTONUP:
            paint = False

    # REDISPLAY
    if paint:
        x, y = pygame.mouse.get_pos()
        screen.blit(brush, (x-16,y-16))
        pygame.display.update()