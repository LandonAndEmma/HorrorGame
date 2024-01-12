"""import pip
pip.main(["install", "pygame"])"""

import pygame
import sys
from inventory import InventorySystem
import csv
CD = pygame.USEREVENT + 1


class Game4:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        self.bg3 = False
        self.bg_cd = False
        self.uncovered = False

        # Set up display
        self.width, self.height = 1920, 1080
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game")

        # Set up colors
        self.white = (255, 255, 255)

        # Load background image
        self.image = pygame.image.load("Sprites/Backgrounds/Corpse Room.png")
        self.key_image = pygame.image.load("Sprites/Items/key.png").convert_alpha()
        self.key_image = pygame.transform.scale(self.key_image, (50, 50))
        self.key_rect = self.key_image.get_rect()

        self.DEFAULT_IMAGE_SIZE = (2600, 2600)
        self.image = pygame.transform.scale(self.image, self.DEFAULT_IMAGE_SIZE)
        self.image_rect = self.image.get_rect()



        # Load item images
        self.next = pygame.image.load("Sprites/Buttons/next2.png").convert_alpha()
        self.next = pygame.transform.scale(self.next, (90, 33))
        self.next_rect = self.next.get_rect()

        self.corpse = pygame.image.load("Sprites/Entities/corpse4.png").convert_alpha()
        self.corpse = pygame.transform.scale(self.corpse, (1235, 897))
        self.corpse_rect = self.corpse.get_rect()

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
            elif event.type == CD:
                self.bg_cd = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self.key_rect.collidepoint(mouse_x, mouse_y) and self.uncovered:
                    self.key_data = "key"
                    self.add_to_csv(self.key_data)
            else:
                self.bg3 = False


    def add_to_csv(self, data):
            with open("data.csv", "a", newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([data])
            # After adding to CSV, update the inventory
            self.inventory_gui.read_csv("data.csv")

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
        self.next_rect.topleft = (self.x + 940, self.y + 1260)

        if self.uncovered:
            self.corpse_rect.topleft = (self.x + 710, self.y + 230)
            self.key_rect.topleft = (self.x + 1150, self.y + 800)
        else:
            self.corpse_rect.topleft = (-1000, -1000)

        # Detect if mouse hovers over

        # Detect if mouse hovers over

    def run(self):
        global game_instance, Game
        # Main game loop
        while True:
            self.handle_events()

            key = pygame.key.get_pressed()
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if key[pygame.K_ESCAPE]:
                f = open("NEW VERSION/data.csv", "w")
                f.truncate()
                f.close()
                pygame.quit()
                sys.exit()
            elif pygame.mouse.get_pressed() == (True, False, False):
                if mouse_y > self.y + 1260:
                    self.bg3 = True
                elif self.x + 1800 > mouse_x > self.x + 700 and self.y + 860 > mouse_y > self.y + 530:
                    with open('data.csv', 'r') as csvfile:
                        my_content = csv.reader(csvfile, delimiter=',')
                        for row in my_content:
                            if "Knife" in row:
                                self.uncovered = True


            # Get mouse position

            self.update_image_position(mouse_x, mouse_y)

            # Draw background
            self.screen.fill(self.white)

            # Draw background image
            self.screen.blit(self.image, self.image_rect)

            # Draw items
            self.screen.blit(self.next, self.next_rect)


            self.screen.blit(self.corpse, self.corpse_rect)
            if self.uncovered:
                self.screen.blit(self.key_image, self.key_rect)


            # Draw inventory GUI
            self.inventory_gui.draw_inventory_gui(500, 500)

            if self.bg3 and self.bg_cd:
                from main3 import Game3
                game_instance = Game3()
                game_instance.run()
                self.bg3 = False
            else:
                self.bg3 = False

            # Update display
            pygame.display.flip()

            # Control the frame rate
            self.clock.tick(30)


if __name__ == "__main__":
    game_instance = Game4()
    game_instance.run()
