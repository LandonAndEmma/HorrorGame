"""import pip
pip.main(["install", "pygame"])"""

import pygame
import sys
from inventory import InventorySystem
import csv


CD = pygame.USEREVENT + 1


class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        self.bg3 = False
        self.bg_cd = False
        self.font = pygame.font.SysFont('arial', 40)

        # Set up display
        self.width, self.height = 1920, 1080
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game")

        # Set up colors
        self.white = (255, 255, 255)

        # Load background image
        self.image = pygame.image.load("Sprites/Backgrounds/Window Room.png")
        self.DEFAULT_IMAGE_SIZE = (2300, 2000)
        self.image = pygame.transform.scale(self.image, self.DEFAULT_IMAGE_SIZE)
        self.image_rect = self.image.get_rect()

        # Load item images
        self.knife = pygame.image.load("Sprites/Items/knife-11.png")
        self.knife_outlined = pygame.image.load("Sprites/Items/knife-11-outlined.png")
        self.knife = pygame.transform.scale(self.knife, (200, 133))
        self.knife_image_rect = self.knife.get_rect()
        self.knife_image = self.knife

        self.box = pygame.image.load("Sprites/Items/box-1.png")
        self.box_outlined = pygame.image.load("Sprites/Items/box-1-outlined.png")
        self.box = pygame.transform.scale(self.box, (83, 133))
        self.box_image_rect = self.box.get_rect()
        self.box_image = self.box

        self.next = pygame.image.load("Sprites/Buttons/next2.png").convert_alpha()
        self.next = pygame.transform.scale(self.next, (90, 33))
        self.next_rect = self.next.get_rect()

        # Set up initial position
        self.x, self.y = self.width - 2000, self.height // 2

        self.image_rect.topleft = (self.x - 200, self.y - 1000)

        self.knife_image_rect.topleft = (self.x + 1000, self.y + 350)

        self.box_image_rect.topleft = (self.x + 930, self.y - 40)

        self.next_rect.topleft = (self.x + 950, self.y + 505)

        # Set up speed
        self.speed = 20

        # Set up stop positions
        self.left_stop_position = -160
        self.right_stop_position = self.width - 1800

        # Text
        self.font = pygame.font.SysFont('arial', 40)

        self.inventory_gui = InventorySystem(self.screen, self.font)
        self.inventory_gui.read_csv("data.csv")

        # Set up clock
        self.clock = pygame.time.Clock()

        pygame.time.set_timer(CD, 1000)

    def add_to_csv(self, data):
        with open("data.csv", "a", newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([data])
        # After adding to CSV, update the inventory
        self.inventory_gui.read_csv("data.csv")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                f = open("NEW VERSION/data.csv", "w")
                f.truncate()
                f.close()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.box_image_rect.collidepoint(event.pos):
                    self.show_full_note = not self.show_full_note
                elif self.knife_image_rect.collidepoint(event.pos):
                    self.knife_data = "Knife"
                    self.add_to_csv(self.knife_data)
                    self.inventory_gui.itemtru = True
                    return self.inventory_gui.itemtru
            elif event.type == CD:
                self.bg_cd = True

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

            # Update image position
            self.image_rect.topleft = (self.x - 200, self.y - 1000)

            # Update item positions
            self.knife_image_rect.topleft = (self.x + 1000, self.y + 350)

            self.box_image_rect.topleft = (self.x + 930, self.y - 40)

            self.next_rect.topleft = (self.x + 950, self.y + 505)

        # Detect if mouse hovers over knife
        if self.x + 1200 > mouse_x > self.x + 1000 and self.y + 450 > mouse_y > self.y + 350:
            self.knife_image = pygame.transform.scale(self.knife_outlined, (200, 133))
        else:
            self.knife_image = pygame.transform.scale(self.knife, (200, 133))

        # Detect if mouse hovers over box
        if self.x + 1010 > mouse_x > self.x + 930 and self.y + 85 > mouse_y > self.y - 40:
            self.box_image = pygame.transform.scale(self.box_outlined, (83, 133))
        else:
            self.box_image = pygame.transform.scale(self.box, (83, 133))

        # If knife has been clicked
       # if self.inventory_gui.itemtru == True:
       #   self.knife_image_rect.topleft = (-100, -100)

    def run(self):
        global game_instance, Game1
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
            elif pygame.mouse.get_pressed() == (True, False, False) and mouse_y > self.y + 500:
                self.bg3 = True
            else:
                self.bg3 = False

            # Get mouse position
            self.update_image_position(mouse_x, mouse_y)

            # Draw background
            self.screen.fill(self.white)

            # Draw background image
            self.screen.blit(self.image, self.image_rect)

            # Draw items
            self.screen.blit(self.knife_image, self.knife_image_rect)
            self.screen.blit(self.box_image, self.box_image_rect)
            self.screen.blit(self.next, self.next_rect)

            # Draw inventory GUI
            self.inventory_gui.draw_inventory_gui(500, 500)

            if self.bg3 and self.bg_cd:
                from main3 import Game3
                game_instance = Game3()
                game_instance.run()
                self.bg3 = False

            # Update display
            pygame.display.flip()

            # Control the frame rate
            self.clock.tick(30)


if __name__ == "__main__":
    game_instance = Game()
    game_instance.run()
