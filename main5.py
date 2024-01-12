

import pygame
import sys
from inventory import InventorySystem
import csv
from pyvidplayer import Video


CD = pygame.USEREVENT + 1


class Game5:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        self.vid = Video("Cutscenes\\good ending.mp4")
        self.vid.set_size((1920, 1080))

        self.bg3 = False
        self.bg_cd = False

        # Set up display
        self.width, self.height = 1920, 1080
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game")

        # Set up colors
        self.white = (255, 255, 255)

        # Load background image
        self.image = pygame.image.load("Sprites/Backgrounds/Operating Room.png")
        self.DEFAULT_IMAGE_SIZE = (2600, 2600)
        self.image = pygame.transform.scale(self.image, self.DEFAULT_IMAGE_SIZE)
        self.image_rect = self.image.get_rect()

        # Load item images
        self.note = pygame.image.load("Sprites/Items/note-11.png")
        self.note_outlined = pygame.image.load("Sprites/Items/note-11-outlined.png")
        self.note = pygame.transform.scale(self.note, (300, 133))
        self.note_image_rect = self.note.get_rect()
        self.note_image = self.note

        self.silhouette_3 = pygame.image.load("Sprites/Entities/creepy-silhouette-3.png")
        self.silhouette_3_outlined = pygame.image.load("Sprites/Entities/creepy-silhouette-3-disappear.png")
        self.silhouette_3 = pygame.transform.scale(self.silhouette_3, (450, 252))
        self.silhouette_3_image_rect = self.silhouette_3.get_rect()
        self.silhouette_3_image = self.silhouette_3

        self.next = pygame.image.load("Sprites/Buttons/next2.png").convert_alpha()
        self.next = pygame.transform.scale(self.next, (90, 33))
        self.next_rect = self.next.get_rect()

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
            else:
                self.bg3 = False


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
        self.note_image_rect.topleft = (self.x + 650, self.y + 440)

        self.silhouette_3_image_rect.topleft = (self.x + 930, self.y - 40)

        self.next_rect.topleft = (self.x + 940, self.y + 1265)

        # Detect if mouse hovers over knife
        if self.x + 890 > mouse_x > self.x + 730 and self.y + 580 > mouse_y > self.y + 450:
            self.note_image = pygame.transform.scale(self.note_outlined, (300, 133))
        else:
            self.note_image = pygame.transform.scale(self.note, (300, 133))

        # Detect if mouse hovers over silhouette


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
            elif pygame.mouse.get_pressed() == (True, False, False) and mouse_y > 1050:
                self.bg3 = True

            # Get mouse position

            if self.x + 1420 > mouse_x > self.x + 930 and self.y + 280 > mouse_y > self.y - 70:
                self.vid.draw(self.screen, (0, 0))
                pygame.display.flip()

            self.update_image_position(mouse_x, mouse_y)

            # Draw background
            self.screen.fill(self.white)

            # Draw background image
            self.screen.blit(self.image, self.image_rect)

            # Draw items
            self.screen.blit(self.note_image, self.note_image_rect)
            self.screen.blit(self.silhouette_3_image, self.silhouette_3_image_rect)
            self.screen.blit(self.next, self.next_rect)

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
    game_instance = Game1()
    game_instance.run()
