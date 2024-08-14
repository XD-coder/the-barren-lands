import tkinter as tk
import random
from PIL import Image, ImageTk, ImageOps
import os

class World:
    def __init__(self, size=10):
        self.size = size
        self.grid = {}
        self.buildings = {}

    def generate_area(self, center, radius=4):
        x_center, y_center = center
        for x in range(x_center - radius, x_center + radius + 1):
            for y in range(y_center - radius, y_center + radius + 1):
                if (x, y) not in self.grid and 0 <= x < self.size and 0 <= y < self.size:
                    self.grid[(x, y)] = self.random_terrain()

    def random_terrain(self):
        terrains = ['.', '.', '.', 'P', 'H']
        return random.choice(terrains)

    def add_building(self, x, y, building_type):
        self.buildings[(x, y)] = Building(building_type=building_type)  # Set the building_type attribute correctly
        print(f"Added {building_type} at ({x}, {y})")

class Building:
    def __init__(self, building_type):
        self.building_type = building_type
        self.advancement_level = 1
        self.advancement_points = 0

    def use(self):
        self.advancement_points += 10
        if self.advancement_points >= self.advancement_level * 100:
            self.level_up()

    def level_up(self):
        self.advancement_level += 1
        self.advancement_points = 0
        print(f"{self.building_type} has leveled up to level {self.advancement_level}!")

    def get_description(self):
        return f"{self.building_type} (Level {self.advancement_level})"

class Player:
    def __init__(self, world):
        self.location = (world.size // 2, world.size // 2)
        world.generate_area(self.location)

    def move(self, direction, world):
        x, y = self.location
        if direction == 'up' and y > 0:
            self.location = (x, y - 1)
        elif direction == 'down' and y < world.size - 1:
            self.location = (x, y + 1)
        elif direction == 'left' and x > 0:
            self.location = (x - 1, y)
        elif direction == 'right' and x < world.size - 1:
            self.location = (x + 1, y)
        else:
            return "You can't move in that direction."
        world.generate_area(self.location)
        return self.describe_location(world)

    def describe_location(self, world):
        terrain = world.grid.get(self.location, '.')
        if terrain == 'P':
            return "You are at a pond. The water looks refreshing."
        elif terrain == 'H':
            return "You found a home. It looks safe."
        elif self.location in world.buildings:
            return world.buildings[self.location].get_description()
        else:
            return "You're standing in barren land."

    def build(self, world, building_type):
        x, y = self.location  # Unpack the tuple into x and y
        if self.location not in world.buildings:
            world.add_building(x, y, building_type)
            return f"You built a {building_type}."
        else:
            return "There's already a building here."


class Game:
    def __init__(self, root):
        self.is_running = True
        self.world = World()
        self.player = Player(self.world)

        self.root = root
        self.root.title("Barren Land")

        # Load and resize the house image
        self.load_image()

        self.chat_frame = tk.Frame(root)
        self.chat_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.text_box = tk.Text(self.chat_frame, state=tk.DISABLED, width=40)
        self.text_box.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.input_frame = tk.Frame(self.chat_frame)
        self.input_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.entry = tk.Entry(self.input_frame)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.process_input)

        self.map_frame = tk.Frame(root)
        self.map_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.map_canvas = tk.Canvas(self.map_frame, width=400, height=400, bg="white")
        self.map_canvas.pack(fill=tk.BOTH, expand=True)

        # Bind arrow keys to movement functions
        self.root.bind("<Up>", lambda event: self.process_arrow_key('up'))
        self.root.bind("<Down>", lambda event: self.process_arrow_key('down'))
        self.root.bind("<Left>", lambda event: self.process_arrow_key('left'))
        self.root.bind("<Right>", lambda event: self.process_arrow_key('right'))

        self.update_map()

    def load_image(self):
        image_path = "./assets/house.png"
        print(f"Attempting to load image from: {image_path}")
        if os.path.exists(image_path):
            try:
                self.house_image = Image.open(image_path)
                print(f"Image loaded successfully: {self.house_image.size}")
                self.house_photo = ImageTk.PhotoImage(self.house_image)
                print("Image converted to PhotoImage successfully.")
            except Exception as e:
                print(f"Error loading image: {e}")
                self.house_photo = None
        else:
            print(f"Image file not found: {image_path}")
            self.house_photo = None


    def process_input(self, event):
        command = self.entry.get().lower()
        if command == "quit":
            self.is_running = False
            self.root.quit()
        elif command.startswith("build"):
            _, building_type = command.split(" ", 1)
            message = self.player.build(self.world, building_type)
            self.add_text(message)
            self.update_map()
        else:
            self.add_text("I don't understand that command.")
        self.entry.delete(0, tk.END)

    def process_arrow_key(self, direction):
        message = self.player.move(direction, self.world)
        self.add_text(message)
        self.update_map()

    def add_text(self, text):
        self.text_box.config(state=tk.NORMAL)
        self.text_box.insert(tk.END, text + "\n")
        self.text_box.config(state=tk.DISABLED)
        self.text_box.yview(tk.END)

    def update_map(self):
        self.map_canvas.delete("all")
        x_center, y_center = self.player.location
        radius = 4
        cell_size = 40

        for y in range(y_center - radius, y_center + radius + 1):
            for x in range(x_center - radius, x_center + radius + 1):
                x_pos = (x - x_center + radius) * cell_size
                y_pos = (y - y_center + radius) * cell_size
                terrain = self.world.grid.get((x, y), ' ')
                color = self.get_terrain_color(terrain)
                print("Buildings in the world:", self.world.buildings)

                # Draw the terrain background
                self.map_canvas.create_rectangle(x_pos, y_pos, x_pos + cell_size, y_pos + cell_size, fill=color, tags="background")

                # Draw the house image if there's a house at this location
                if (x, y) in self.world.buildings and self.world.buildings[(x, y)].building_type == "house":
                    if self.house_photo:
                        print(f"Drawing house at ({x}, {y}) on canvas.")
                        self.map_canvas.create_image(x_pos, y_pos, anchor=tk.NW, image=self.house_photo, tags="building")
                else:
                    print("House image not loaded properly.")
                # Draw the player
                if (x, y) == self.player.location:
                    self.map_canvas.create_text(x_pos + cell_size // 2, y_pos + cell_size // 2, text="X", tags="player")

    def get_terrain_color(self, terrain):
        if terrain == 'P':
            return "blue"
        elif terrain == 'H':
            return "brown"
        elif terrain == '.':
            return "green"
        else:
            return "white"

def main():
    root = tk.Tk()
    game = Game(root)
    root.mainloop()

if __name__ == "__main__":
    main()
