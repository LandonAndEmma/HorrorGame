"""import pip
pip.main(["install", "pygame"])"""

import pygame
import sys
from inventory import InventorySystem
import csv

CD = pygame.USEREVENT + 1


class Game2:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        self.next_bg = False
        self.bg_cd = False
        self.show_arrow = False
        # Set up display
        self.width, self.height = 1920, 1080
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game")
        self.trapdoor_open = False

        # Set up colors
        self.white = (255, 255, 255)

        # Load background image
        self.image = pygame.image.load("Sprites\\Backgrounds\\Bathroom.png")
        self.DEFAULT_IMAGE_SIZE = (2300, 2000)
        self.image = pygame.transform.scale(self.image, self.DEFAULT_IMAGE_SIZE)
        self.image_rect = self.image.get_rect()

        self.arrow_image = pygame.image.load("Sprites\\Buttons\\next2.png").convert_alpha()
        self.arrow_image = pygame.transform.scale(self.arrow_image, (50, 50))
        self.arrow_rect = self.arrow_image.get_rect()

        # Load item images
        self.trapdoor = pygame.image.load("Sprites\\Items\\trapdoor-1.png").convert_alpha()
        self.trapdoor = pygame.transform.scale(self.trapdoor, (400, 198))
        self.trapdoor_rect = self.trapdoor.get_rect()

        self.next = pygame.image.load("Sprites\\Buttons\\next2.png").convert_alpha()
        self.next = pygame.transform.scale(self.next, (90, 33))
        self.next_rect = self.next.get_rect()

        # Set up initial position
        self.x, self.y = self.width - 2000, self.height // 2

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

        # Text
        self.font = pygame.font.SysFont('arial', 40)
        self.text = self.font.render("This seems to be jammed shut...", True, "black", None)
        self.textrect = self.text.get_rect()
        self.textrect.center = (1400, 800)

        self.clicked_trapdoor = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                f = open("NEW VERSION\\data.csv", "w")
                f.truncate()
                f.close()
                pygame.quit()
                sys.exit()
            elif event.type == CD:
                self.bg_cd = True

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
            self.next_rect.topleft = (self.x + 1040, self.y + 500)

            self.trapdoor_rect.topleft = (self.x + 1700, self.y + 400)

            if self.trapdoor_open:
                self.trapdoor_rect.topleft = (-20000, -20000)
                self.text = self.font.render("", True, "black", None)

        # Detect if user clicks
        if self.x + 2100 > mouse_x > self.x + 1750 and self.y + 600 > mouse_y > self.y + 400 and \
                pygame.mouse.get_pressed() == (True, False, False):
            self.clicked_trapdoor = True

    def run(self):
        global game_instance, Game1
        # Main game loop
        while True:
            self.handle_events()
            if self.show_arrow:
                self.arrow_rect.topleft = (self.x + 1800, self.y + 400)
                self.screen.blit(self.arrow_image, self.arrow_rect)
                # Check if the arrow is clicked
                if self.arrow_rect.collidepoint(mouse_x, mouse_y) and pygame.mouse.get_pressed() == (True, False, False):
                    # Switch to Game5
                    from main5 import Game5
                    game_instance = Game5()
                    game_instance.run()

            key = pygame.key.get_pressed()
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if key[pygame.K_ESCAPE]:
                f = open("data.csv", "w")
                f.truncate()
                f.close()
                pygame.quit()
                sys.exit()
            elif pygame.mouse.get_pressed() == (True, False, False) and mouse_y > self.y + 500:
                self.next_bg = True
            else:
                self.next_bg = False

            self.update_image_position(mouse_x, mouse_y)

            # Draw background
            self.screen.fill(self.white)

            # Draw background image
            self.screen.blit(self.image, self.image_rect)




            with open('data.csv', 'r') as csvfile:
                my_content = csv.reader(csvfile, delimiter=',')
                for row in my_content:
                    # Blit text if trapdoor is clicked without key
                    if self.clicked_trapdoor:
                        if "key" in row:
                            self.trapdoor_open = True
                            self.text = self.font.render("", True, "black", None)
                            self.trapdoor_rect.topleft = (-20000, -20000)
                            self.clicked_trapdoor = False
                            self.show_arrow = True

                            # Display text only if "key" is not in the CSV file


            if self.show_arrow:
                self.arrow_rect.topleft = (self.x + 1800, self.y + 400)
                self.screen.blit(self.arrow_image, self.arrow_rect)

            # Draw items
            self.screen.blit(self.trapdoor, self.trapdoor_rect)

            self.screen.blit(self.next, self.next_rect)

            # Draw inventory GUI
            self.inventory_gui.draw_inventory_gui(500, 500)

            if self.next_bg and self.bg_cd:
                from main3 import Game3
                game_instance = Game3()
                game_instance.run()
                self.next_bg = False

            # Update display
            pygame.display.flip()

            # Control the frame rate
            self.clock.tick(30)


if __name__ == "__main__":
    game_instance = Game2()
    game_instance.run()
