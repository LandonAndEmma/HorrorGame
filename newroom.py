"""import pip
pip.main(["install", "pygame"])"""

import pygame
import sys
from inventory import InventorySystem

CD = pygame.USEREVENT + 1


class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        self.next_bg = False
        self.bg_cd = False
        self.itemtru = False

        # Set up display
        self.width, self.height = 1920, 1080
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game")

        # Set up colors
        self.white = (255, 255, 255)

        # Load background image
        self.image = pygame.image.load("Sprites\Backgrounds\Ruined")
        self.DEFAULT_IMAGE_SIZE = (2300, 2000)
        self.image = pygame.transform.scale(self.image, self.DEFAULT_IMAGE_SIZE)
        self.image_rect = self.image.get_rect()

        # Load item images
        self.knife = pygame.image.load("Sprites\Items\knife-1.png")
        self.knife_outlined = pygame.image.load("Sprites\Items\knife-1-outlined.png")
        self.knife = pygame.transform.scale(self.knife, (200, 133))
        self.knife_image_rect = self.knife.get_rect()
        self.knife_image = self.knife

        self.box = pygame.image.load("Sprites\\Items\\box-1.png")
        self.box_outlined = pygame.image.load("Sprites\\Items\\box-1-outlined.png")
        self.box = pygame.transform.scale(self.box, (83, 133))
        self.box_image_rect = self.box.get_rect()
        self.box_image = self.box

        self.next = pygame.image.load("Sprites\\Buttons\\next.png").convert_alpha()
        self.next = pygame.transform.scale(self.next, (33, 90))
        self.next_rect = self.next.get_rect()

        # Set up initial position
        self.x, self.y = self.width - 2000, self.height // 2

        # Set up speed
        self.speed = 20

        self.font = pygame.font.Font("Fonts\\Note Font.ttf", 36)
        # Set up stop positions
        self.left_stop_position = -160
        self.right_stop_position = self.width - 1800
        self.inventory_gui = InventorySystem(self.screen, self.font)
        # Set up clock
        self.clock = pygame.time.Clock()
        self.show_full_note = False
        pygame.time.set_timer(CD, 1000)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == CD:
                self.bg_cd = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.box_image_rect.collidepoint(event.pos):
                    self.show_full_note = not self.show_full_note
                elif self.knife_image_rect.collidepoint(event.pos):
                    self.add_to_inventory("Knife")
                    self.itemtru = True
                elif self.show_full_note and self.close_button_rect.collidepoint(event.pos):
                    self.show_full_note = False

    def add_to_inventory(self, item):
        self.inventory_gui.add_item(item)
        print(f"Added {item} to inventory: {self.inventory_gui.inventory}")

    def read_text_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Error: File not found - {file_path}")
            return ""

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

            self.next_rect.topleft = (self.x + 2040, self.y - 40)

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

        if self.itemtru == True:
            self.knife_image_rect.topleft = (-100, -100)
    def run(self):
        global game_instance, Game1
        # Main game loop
        while True:
            self.handle_events()

            key = pygame.key.get_pressed()
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if key[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
            elif pygame.mouse.get_pressed() == (True, False, False) and mouse_x > 1870:
                self.next_bg = True
            else:
                self.next_bg = False

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

            if self.next_bg and self.bg_cd:
                from main1 import Game1
                game_instance = Game1()
                game_instance.run()
                self.next_bg = False
            self.inventory_gui.draw()
            # Update display
            pygame.display.flip()

            # Control the frame rate
            self.clock.tick(30)


if __name__ == "__main__":
    game_instance = Game()
    game_instance.run()
