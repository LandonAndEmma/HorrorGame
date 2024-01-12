

import pygame
import sys





class Game1:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up display
        self.width, self.height = 1920, 1080
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game")

        # Set up colors
        self.white = (255, 255, 255)


        # Room Chercker thang
        self.next_bg = False
        self.last_right_arrow_press_time = 0
        self.right_arrow_cooldown = 2000

        # Load background image
        self.image = pygame.image.load("Sprites\Backgrounds\Operating Room.png")
        self.DEFAULT_IMAGE_SIZE = (2600, 2600)
        self.image = pygame.transform.scale(self.image, self.DEFAULT_IMAGE_SIZE)
        self.image_rect = self.image.get_rect()

        # Load item images
        self.note = pygame.image.load("Sprites\Items\\note-1.png")
        self.note_outlined = pygame.image.load("Sprites\\Items\\note-1-outlined.png")
        self.note = pygame.transform.scale(self.note, (300, 133))
        self.note_image_rect = self.note.get_rect()
        self.note_image = self.note

        self.silhouette_3 = pygame.image.load("Sprites\\Entities\\creepy-silhouette-3.png")
        self.silhouette_3_outlined = pygame.image.load("Sprites\\Entities\\creepy-silhouette-3-disappear.png")
        self.silhouette_3 = pygame.transform.scale(self.silhouette_3, (450, 252))
        self.silhouette_3_image_rect = self.silhouette_3.get_rect()
        self.silhouette_3_image = self.silhouette_3

        # Set up initial position
        self.x, self.y = self.width - 2000, self.height - 540

        # Set up speed
        self.speed = 20

        # Set up stop positions
        self.left_stop_position = -160
        self.right_stop_position = self.width - 1800
        self.top_stop_position = 760
        self.bottom_stop_position = self.height - 1300

        # Set up clock
        self.clock = pygame.time.Clock()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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

        # Detect if mouse hovers over knife
        if self.x + 890 > mouse_x > self.x + 730 and self.y + 580 > mouse_y > self.y + 450:
            self.note_image = pygame.transform.scale(self.note_outlined, (300, 133))
        else:
            self.note_image = pygame.transform.scale(self.note, (300, 133))

        # Detect if mouse hovers over silhouette
        if self.x + 1420 > mouse_x > self.x + 930 and self.y + 280 > mouse_y > self.y - 70:
            self.silhouette_3_image = pygame.transform.scale(self.silhouette_3_outlined, (450, 252))
        else:
            self.silhouette_3_image = pygame.transform.scale(self.silhouette_3, (450, 252))

    def run(self):
        global game_instance

        # Main game loop
        while True:
            self.handle_events()
            key = pygame.key.get_pressed()

            if key[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
            elif key[pygame.K_RIGHT]:
                current_time = pygame.time.get_ticks()
                # Check if the cooldown has elapsed
                if current_time - self.last_right_arrow_press_time > self.right_arrow_cooldown:
                    # Trigger the action
                    self.last_right_arrow_press_time = current_time
                    self.next_bg = True

            # Get mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()

            self.update_image_position(mouse_x, mouse_y)

            # Draw background
            self.screen.fill(self.white)

            # Draw background image
            self.screen.blit(self.image, self.image_rect)

            # Draw items
            self.screen.blit(self.note_image, self.note_image_rect)
            self.screen.blit(self.silhouette_3_image, self.silhouette_3_image_rect)

            if self.next_bg:
                from mainver1 import Bedroom2
                print(self.next_bg)
                self.next_bg = False
                print(self.next_bg)
                game_instance = Bedroom2()
                game_instance.run()


            # Update display
            pygame.display.flip()

            # Control the frame rate
            self.clock.tick(30)

