# IDEA
# Import and Initialize
import pygame, random
from pygame.locals import *
pygame.init()

# Display configuration
size = (640,480)
screen = pygame.display.set_mode(size)
screen.fill((255,255,255))
pygame.display.set_caption('Hau den Maulwurf')

# Entities
class Mole(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/mole.png')
        self.image = pygame.transform.scale(self.image, (100,100))
        self.rect = self.image.get_rect()
        self.sound = pygame.mixer.Sound('sounds/cry.mp3')
        self.rect.lef = random.randint(0,620)
        self.rect.top = random.randint(0, 460)

    def flee(self):
        self.rect.lef = random.randint(0,620)
        self.rect.top = random.randint(0, 460)

    def cry(self):
        self.sound.play()

    def hit(self,pos):
        return self.rect.collidepoint(pos)

class Shovel(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/schaufel.png')
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.rect.center = pygame.mouse.get_pos()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()


mole = Mole()
shovel = Shovel()

sprite_group = pygame.sprite.Group()
sprite_group.add(mole)
sprite_group.add(shovel)

bg = pygame.image.load('images/background_grass.png')
bg = pygame.transform.scale(bg, size)

bg_red = pygame.Surface(size)
bg_red = bg_red.convert()
bg_red.fill((255,0,0))

font = pygame.font.Font(None, 255)

# Action
# ALTER

# VARIABLES
keepGoing = True
ctr = 0
clock = pygame.time.Clock()
pygame.time.set_timer(USEREVENT, 200)

# LOOP
while keepGoing:
    # TIMER
    clock.tick(30)

    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == QUIT:
            keepGoing = False
            break
        elif event.type == MOUSEBUTTONDOWN:
            if mole.hit(pygame.mouse.get_pos()):
                mole.cry()
                ctr += 1
                screen.blit(bg_red, (0,0))
                break
        elif event.type == USEREVENT:
            mole.flee()
            pygame.time.set_timer(USEREVENT, 1000)
            screen.blit(bg, (0,0))
            sprite_group.update()
            sprite_group.draw(screen)
            text = font.render(u"Maulwürfe: " + str(ctr), True, Color("white"))
            screen.blit(text, (10,230))

    # REDISPLAY
    pygame.display.flip()
