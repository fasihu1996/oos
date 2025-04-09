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
brush_size = 128
brush_size_tuple = (brush_size, brush_size)
brush_black = pygame.image.load('./images/black_brush.png')
brush_black = pygame.transform.scale(brush_black, brush_size_tuple)
brush_red = pygame.image.load('./images/red_brush.png')
brush_red = pygame.transform.scale(brush_red, brush_size_tuple)
brush_yellow = pygame.image.load('./images/yellow_brush.png')
brush_yellow = pygame.transform.scale(brush_yellow, brush_size_tuple)


selectedBrush = brush_black
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
        elif event.type == KEYDOWN:
            if event.key == K_s:
                pygame.image.save(screen, "screenhot.png")
            elif event.key == K_r:
                selectedBrush = brush_red
            elif event.key == K_b:
                selectedBrush = brush_black
            elif event.key == K_y:
                selectedBrush = brush_yellow
            elif event.key == K_p:
                brush_size *= 2
                brush_size_tuple = (brush_size, brush_size)
            elif event.key == K_m:
                brush_size /= 2
                brush_size_tuple = (brush_size, brush_size)


            
    # Refresh Display  
    if paint:
        # screen.blit(bg, (0, 0)) 
        screen.blit(selectedBrush, (x-64, y-64))
        pygame.display.update()
    
    
      
      
