import pygame
import sys

from pygame.locals import *

# IMPORT INITIALIZE
# Pygame initialisieren
pygame.init()
# DISPLAY CONFIGURATION
# Fenstergröße festlegen
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Fügen Sie hier den Titel des Fensters hinzu
pygame.display.set_caption("Hau den Maulwurf")

# ENTITIES


# Farben
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Rechtecke erstellen (Position und Größe)
rect1 = pygame.Rect(100, 100, 100, 100)  # x, y, width, height
rect2 = pygame.Rect(300, 300, 100, 100)

# Geschwindigkeit für rect1
rect1_speed_x = rect1_speed_y = 0
movement_speed = 5

# ACTION
# ALTER

# Hauptspiel-Schleife
running = True
clock = pygame.time.Clock()

# LOOP

while running:

    # TIMER
    clock.tick(60)

    # EVENT HANDLING
    # Ereignisse durchlaufen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Rechteck 1 bewegen
        rect1.x += rect1_speed_x
        rect1.y += rect1_speed_y

        # Tasten drücken
        if event.type == pygame.KEYDOWN:
            # Fügen Sie hier die Tastenbehandlung für die Bewegung von rect1 hinzu
            # pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN
            if event.key == K_DOWN:
                print(rect1.bottom)
                if rect1.bottom < 600:
                    rect1_speed_y = movement_speed

            if event.key == K_UP:
                if rect1.top > 0:
                    rect1_speed_y = -movement_speed

            if event.key == K_LEFT:
                if rect1.left > 0:
                    rect1_speed_x = -movement_speed

            if event.key == K_RIGHT:
                if rect1.right < 800:
                    rect1_speed_x = movement_speed

        # Tasten loslassen
        if event.type == pygame.KEYUP:
            # Fügen Sie hier die Tastenbehandlung für die Bewegung von rect1 hinzu
            # pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN
            rect1_speed_x = rect1_speed_y = 0
            pass

    # Rechteck 1 bewegen
    rect1.x += rect1_speed_x
    rect1.y += rect1_speed_y

    if rect1.left < 0:
        rect1.left = 0
    if rect1.right > 800:
        rect1.right = 800
    if rect1.top < 0:
        rect1.top = 0
    if rect1.bottom > 600:
        rect1.bottom = 600
    # Bei einer Kollision "Kollision!" auf der Konsole ausgeben
    if rect1.colliderect(rect2):
        print("Kollision!")

    # Bildschirm füllen (Hintergrund)
    screen.fill(WHITE)

    # Rechtecke zeichnen
    pygame.draw.rect(screen, RED, rect1)
    pygame.draw.rect(screen, BLUE, rect2)

    # REDISPLAY
    # Bildschirm aktualisieren
    pygame.display.flip()
