from pygame import *
import pygame
from settings import *
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Moondew Canyon")
        self.clock = pygame.time.Clock()
        self.running = True
        self.level = Level()

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000

            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    self.running = False

            self.level.run(dt)
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()