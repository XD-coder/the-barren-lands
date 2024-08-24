class Terrain:
    def __init__(self, terrain_type):
        self.terrain_type = terrain_type
        self.commands = {}  # Commands specific to the terrain

    def get_description(self):
        return f"You are standing on {self.terrain_type}."


class Pond(Terrain):
    def __init__(self):
        super().__init__("Pond")
        self.commands = {"drink": self.drink_water}

    def drink_water(self):
        return "You drink water from the pond. It's refreshing!"
