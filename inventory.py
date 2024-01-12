
import csv

class InventorySystem:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.inventory = []

    def read_csv(self, filename):
        with open(filename, newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                self.inventory.append(row[0])  # Assuming the CSV file contains single values per row

    def draw_inventory_gui(self, x, y):
        # Display everything in the inventory without duplicates on the screen
        unique_items = set(self.inventory)  # Use a set to remove duplicates
        for i, item in enumerate(unique_items):
            text = self.font.render(item, True, (255, 255, 255))  # Use white text
            self.screen.blit(text, (x, y + i * 40))  # Adjust the position based on your layout
