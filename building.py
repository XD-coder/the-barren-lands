class Building:
    def __init__(self, building_type):
        self.building_type = building_type
        self.advancement_level = 1
        self.advancement_points = 0
        self.commands = {}  # Commands specific to the building

    def use(self):
        self.advancement_points += 10
        if self.advancement_points >= self.advancement_level * 100:
            return self.level_up()

    def level_up(self):
        self.advancement_level += 1
        self.advancement_points = 0
        return f"{self.building_type} has leveled up to level {self.advancement_level}!"

    def get_description(self):
        return f"{self.building_type} (Level {self.advancement_level})"


class House(Building):
    def __init__(self):
        super().__init__("House")
        self.commands = {"rest": self.rest_in_house}

    def rest_in_house(self):
        return "You rest in the house and regain energy."
