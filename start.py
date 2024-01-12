import pip
pip.main(["install", "pygame"])

import pygame
import sys

from inventory import InventorySystem
class Start:
    def __init__(self):
        # Initialize Pygame
        pygame.init()



        # Set up display
        self.width, self.height = 1920, 1080
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game")

        # Set up colors
        self.bg = (20, 20, 20)

        self.start = pygame.image.load("/home/roi/Downloads/NEW VERSION/Sprites/Buttons/start-game.png")
        self.start = pygame.transform.scale_by(self.start, (.505, .505))
        self.start_pos = (self.width // 2 - 310, 200)
        self.start_rect = self.start.get_rect()

        self.options = pygame.image.load("Sprites/Buttons/options.png")
        self.options = pygame.transform.scale_by(self.options, (.5, .5))
        self.options_pos = (self.width // 2 - 310, 500)
        self.options_rect = self.options.get_rect()

        self.start_game = False

        # Set up clock
        self.clock = pygame.time.Clock()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def run(self):
        global game_instance
        while True:
            self.handle_events()

            key = pygame.key.get_pressed()

            if key[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

            x, y = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed() == (True, False, False) and \
                    self.width // 2 - 310 < x < self.width // 2 + 295 and 200 < y < 400:
                self.start_game = True

            if self.start_game:
                from main3 import Game3
                game_instance = Game3()
                game_instance.run()
                self.start_game = False

            # Draw background
            self.screen.fill(self.bg)

            self.screen.blit(self.start, self.start_pos)
            self.screen.blit(self.options, self.options_pos)

            # Update display
            pygame.display.flip()

            # Control the frame rate
            self.clock.tick(30)


if __name__ == "__main__":
    game_instance = Start()
    game_instance.run()
