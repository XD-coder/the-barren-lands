# world.py
import random
from terrain import Terrain, Pond  # Import the necessary classes from terrain.py
from building import House         # Import buildings from building.py

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
                    terrain = self.random_terrain()
                    self.grid[(x, y)] = terrain
                    if isinstance(terrain, House):
                        self.buildings[(x, y)] = terrain  # Add building if it's a house

    def random_terrain(self):
        terrains = [Terrain('grass land'), Terrain('grass land'), Terrain('dessert'), Pond(), House()]
        return random.choice(terrains)
