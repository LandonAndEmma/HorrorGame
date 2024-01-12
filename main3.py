"""import pip
pip.main(["install", "pygame"])"""

import pygame
import sys
from inventory import InventorySystem
import csv


CD = pygame.USEREVENT + 1


class Game3:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        self.next_bg = False
        self.bg = False
        self.bg1 = False
        self.bg2 = False
        self.bg4 = False
        self.bg_cd = False

        # Set up display
        self.width, self.height = 1920, 1080
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game")

        # Set up colors
        self.white = (255, 255, 255)

        # Load background image
        self.image = pygame.image.load("Sprites/Backgrounds/Hallway.png")
        self.DEFAULT_IMAGE_SIZE = (2600, 2600)
        self.image = pygame.transform.scale(self.image, self.DEFAULT_IMAGE_SIZE)
        self.image_rect = self.image.get_rect()

        # Load next arrows
        self.next = pygame.image.load("Sprites/Buttons/next1.png").convert_alpha()
        self.next = pygame.transform.scale(self.next, (33, 90))
        self.next_rect = self.next.get_rect()

        self.next1 = pygame.image.load("Sprites/Buttons/next1.png").convert_alpha()
        self.next1 = pygame.transform.scale(self.next1, (33, 90))
        self.next1_rect = self.next1.get_rect()

        self.next2 = pygame.image.load("Sprites/Buttons/next1.png").convert_alpha()
        self.next2 = pygame.transform.scale(self.next2, (33, 90))
        self.next2_rect = self.next2.get_rect()

        self.next4 = pygame.image.load("Sprites/Buttons/next1.png").convert_alpha()
        self.next4 = pygame.transform.scale(self.next4, (33, 90))
        self.next4_rect = self.next4.get_rect()

        # Set up initial position
        self.x, self.y = self.width - 2000, self.height - 540

        # Set up speed
        self.speed = 20

        # Set up stop positions
        self.left_stop_position = -160
        self.right_stop_position = self.width - 1800
        self.top_stop_position = 760
        self.bottom_stop_position = self.height - 1300

        # Text
        self.font = pygame.font.SysFont('arial', 40)

        self.inventory_gui = InventorySystem(self.screen, self.font)
        self.inventory_gui.read_csv("data.csv")

        # Set up clock
        self.clock = pygame.time.Clock()

        pygame.time.set_timer(CD, 1000)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                f = open("data.csv", "w")
                f.truncate()
                f.close()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x = 'donothing'
            elif event.type == CD:
                self.bg_cd = True
            else:
                self.next_bg = False



    def add_to_inventory(self, item):
        self.inventory_gui.add_item(item)
        print(f"Added {item} to inventory: {self.inventory_gui.inventory}")

    def update_image_position(self, mouse_x, mouse_y):
        if (mouse_x < self.width // 2 - 200 and self.x < self.right_stop_position) or \
                (mouse_x > self.width // 2 + 200 and self.x > self.left_stop_position):
            # Update image position based on mouse position
            if mouse_x < self.width // 2:
                self.x += self.speed
            else:
                self.x -= self.speed

        if (mouse_y < self.height // 2 - 200 and self.y < self.top_stop_position) or \
                (mouse_y > self.height // 2 + 200 and self.y > self.bottom_stop_position):
            # Update image position based on mouse position
            if mouse_y < self.height // 2:
                self.y += self.speed
            else:
                self.y -= self.speed

        # Update image position
        self.image_rect.topleft = (self.x - 200, self.y - 1000)

        # Update item positions
        self.next_rect.topleft = (self.x + 1940, self.y + 160)
        self.next1_rect.topleft = (self.x + 1640, self.y + 215)
        self.next2_rect.topleft = (self.x + 1440, self.y + 250)
        self.next4_rect.topleft = (self.x + 1095, self.y + 240)

        # If {item} has been clicked

    def run(self):
        global game_instance, Game
        # Main game loop
        while True:
            self.handle_events()

            key = pygame.key.get_pressed()
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if key[pygame.K_ESCAPE]:
                f = open("data.csv", "w")
                f.truncate()
                f.close()
                pygame.quit()
                sys.exit()
            elif pygame.mouse.get_pressed() == (True, False, False):
                if self.x + 1155 > mouse_x > self.x + 1067 and self.y + 340 > mouse_y > self.y + 234:
                    self.bg = True
                elif self.x + 1523 > mouse_x > self.x + 1424 and self.y + 588 > mouse_y > self.y + 121:
                    self.bg1 = True
                elif self.x + 1689 > mouse_x > self.x + 1613 and self.y + 655 > mouse_y > self.y + 65:
                    self.bg2 = True
                elif self.x + 2009 > mouse_x > self.x + 1854 and self.y + 657 > mouse_y > self.y - 45:
                    self.bg4 = True
            print(pygame.mouse.get_pos())
            print("x: ")
            print(self.x)
            print("y: ")
            print(self.y)

            # Get mouse position

            self.update_image_position(mouse_x, mouse_y)

            # Draw background
            self.screen.fill(self.white)

            # Draw background image
            self.screen.blit(self.image, self.image_rect)

            # Draw items
            self.screen.blit(self.next, self.next_rect)
            self.screen.blit(self.next1, self.next1_rect)
            self.screen.blit(self.next2, self.next2_rect)
            self.screen.blit(self.next4, self.next4_rect)

            # Draw inventory
            self.inventory_gui.draw_inventory_gui(500, 500)

            if self.next_bg and self.bg_cd:
                from main4 import Game4
                game_instance = Game4()
                game_instance.run()
                self.next_bg = False
            else:
                self.next_bg = False
            if self.bg and self.bg_cd:
                from main import Game
                game_instance = Game()
                game_instance.run()
                self.bg = False
            elif self.bg1 and self.bg_cd:
                from main1 import Game1
                game_instance = Game1()
                game_instance.run()
                self.bg1 = False
            elif self.bg2 and self.bg_cd:
                from main2 import Game2
                game_instance = Game2()
                game_instance.run()
                self.bg2 = False
            elif self.bg4 and self.bg_cd:
                from main4 import Game4
                game_instance = Game4()
                game_instance.run()
                self.bg4 = False


            # Update display
            pygame.display.flip()

            # Control the frame rate
            self.clock.tick(30)


if __name__ == "__main__":
    game_instance = Game3()
    game_instance.run()
