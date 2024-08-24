# game.py
import tkinter as tk
from player import Player
from world import World
from building import House  # Import the House class
from PIL import Image, ImageTk
from terrain import Terrain
import os


class Game:
    def __init__(self, root):
        self.is_running = True
        self.world = World()
        self.player = Player(self.world)

        self.root = root
        self.root.title("Barren Land")

        # Set up the GUI elements
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

        # Initialize the map canvas before load_image and update_map
        self.map_canvas = tk.Canvas(self.map_frame, width=400, height=400, bg="white")
        self.map_canvas.pack(fill=tk.BOTH, expand=True)

        # Bind arrow keys
        self.root.bind("<Up>", lambda event: self.process_arrow_key('up'))
        self.root.bind("<Down>", lambda event: self.process_arrow_key('down'))
        self.root.bind("<Left>", lambda event: self.process_arrow_key('left'))
        self.root.bind("<Right>", lambda event: self.process_arrow_key('right'))

        # Now load the image and update the map
        self.load_image()
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
                self.house_photo = None  # Ensure house_photo is None if loading fails
        else:
            print(f"Image file not found: {image_path}")
            self.house_photo = None


    def process_input(self, event):
        command = self.entry.get().lower()
        if command == "quit":
            self.is_running = False
            self.root.quit()
        else:
            message = self.player.execute_command(command, self.world)
            self.add_text(message)
        self.update_map()
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

                # Get the terrain object or None if there's no terrain at that location
                terrain = self.world.grid.get((x, y))

                # Determine the color based on terrain or use a default color if there's no terrain
                if terrain and isinstance(terrain, Terrain):
                    color = self.get_terrain_color(terrain.terrain_type)
                else:
                    color = "white"  # Default background color if no terrain

                # Draw the background cell
                self.map_canvas.create_rectangle(x_pos, y_pos, x_pos + cell_size, y_pos + cell_size, fill=color, tags="background")

                # Check if there's a building at this location
                if (x, y) in self.world.buildings:
                    building = self.world.buildings[(x, y)]
                    if isinstance(building, House) and self.house_photo:
                        self.map_canvas.create_image(x_pos + cell_size // 2, y_pos + cell_size // 2, image=self.house_photo)
                    else:
                        # Handle other types of buildings if needed
                        pass

                # Draw the player
                if (x, y) == self.player.location:
                    self.map_canvas.create_text(x_pos + cell_size // 2, y_pos + cell_size // 2, text="X", tags="player")

    
    def get_terrain_color(self, terrain_type):
        if terrain_type == 'Pond':
            return "blue"
        elif terrain_type == 'House':
            return "brown"
        elif terrain_type == 'grass land':
            return "green"
        elif terrain_type == 'dessert':
            return "goldenrod3"
        else:
            return "white"

def main():
    root = tk.Tk()
    game = Game(root)
    root.mainloop()

if __name__ == "__main__":
    main()
