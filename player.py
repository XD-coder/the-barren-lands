from terrain import Terrain 
class Player:
    def __init__(self, world):
        self.location = (world.size // 2, world.size // 2)  # Start in the center of the world
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
        
        world.generate_area(self.location)  # Generate new terrain when moving
        return self.describe_location(world)

    def describe_location(self, world):
        terrain = world.grid.get(self.location, Terrain('.'))
        if self.location in world.buildings:
            return world.buildings[self.location].get_description()
        return terrain.get_description()

    def execute_command(self, command, world):
        if self.location in world.buildings:
            building = world.buildings[self.location]
            if command in building.commands:
                return building.commands[command]()
        
        terrain = world.grid.get(self.location)
        if command in terrain.commands:
            return terrain.commands[command]()
        
        return "This command can't be used here."
