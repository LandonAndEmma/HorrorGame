import pygame
import sys



class Hallway:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("sfx/ambience/cable_noise.wav"), loops=-1)

        # Set up display
        self.width, self.height = 1920, 1080
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Hallway")

        # Set up colors
        self.white = (255, 255, 255)
        # Arrow clicked checker thang
        self.left_button_clicked = False
        self.last_right_arrow_press_time = 1000
        self.right_arrow_cooldown = 2000
        # Next Room Switcher thang
        self.next_bg = False

        # Load images
        self.image = pygame.image.load("Sprites/backgrounds/ruined_hallway.png")
        self.left_button_img = pygame.image.load("Sprites/ui/left_arrow.png")
        self.DEFAULT_IMAGE_SIZE = (2300, 2000)
        self.DEFAULT_ITEM_SIZE = (80, 160)
        self.image = pygame.transform.scale(self.image, self.DEFAULT_IMAGE_SIZE)
        self.image_rect = self.image.get_rect()
        self.left_button_rect = self.left_button_img.get_rect()


        # Set up initial position
        self.x, self.y = self.width - 2000, self.height // 2

        # Set up speed
        self.speed = 20


        # Set up stop positions
        self.left_stop_position = -160
        self.right_stop_position = self.width - 1800

        # Set up clock
        self.clock = pygame.time.Clock()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.left_button_rect.collidepoint(event.pos):
                    # Set the variable to True when the left button is clicked
                    self.left_button_clicked = True



    def update_image_position(self, mouse_x):
        if (mouse_x < self.width // 2 - 200 and self.x < self.right_stop_position) or \
           (mouse_x > self.width // 2 + 200 and self.x > self.left_stop_position):
            # Update image position based on mouse position
            if mouse_x < self.width // 2:
                self.x += self.speed
            else:
                self.x -= self.speed

            # Update image position
            self.image_rect.topleft = (self.x - 200, self.y - 1000)
            self.left_button_rect.topleft = (self.x + 9, self.y - 50)



    def read_text_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Error: File not found - {file_path}")
            return ""

    def get_left_button_state(self):
        return self.left_button_clicked


    def run(self):
        global game_instance
        global next_bg


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

            self.update_image_position(mouse_x)

            # Draw background
            self.screen.fill(self.white)

            # Draw image
            self.screen.blit(self.image, self.image_rect)
            self.screen.blit(self.left_button_img, self.left_button_rect.topleft)

            if self.next_bg:
                from mainver1_1 import Game1
                self.next_bg = False
                game_instance = Game1()
                game_instance.run()



            # Update display
            pygame.display.flip()

            # Control the frame rate
            self.clock.tick(30)
