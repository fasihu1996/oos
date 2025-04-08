# IDEA
# Import and Init
import pygame
from pygame.locals import *

pygame.init()

# Display
size = width, height = 640, 480
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))
pygame.display.set_caption('Paint Brush')

# Entities
# bg = pygame.image.load('./images/world.jpg') # Background images
# screen.blit(bg, (0, 0)) 

brush = pygame.image.load('./images/blackBrush.gif')
brush = pygame.transform.scale(brush, (128,128))
# brushRect = brush.get_rect()
pygame.display.update()

# Loop == ALTER
# Assign Values to key variables
keepGoing = True
paint = False
clock = pygame.time.Clock()

# Loop
while keepGoing:
    # Timing
    clock.tick(30) 
    
    # Events
    x, y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            keepGoing = False
            break
        elif event.type == MOUSEBUTTONDOWN:
            paint = True
        elif event.type == MOUSEBUTTONUP:
            paint = False
        elif event.type == KEYDOWN and event.key == K_SPACE:
            pygame.image.save(screen, "screenhot.") 
            
    # Refresh Display  
    if paint:
        # screen.blit(bg, (0, 0)) 
        screen.blit(brush, (x-64, y-64))
        pygame.display.update()
    
    
      
      
