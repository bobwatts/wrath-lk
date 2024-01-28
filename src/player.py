import json


class Player:
    def __init__(self, hero):
        self.hand = []
        self.hero = hero
        json_file_path = "./data/herodata.json"
        with open(json_file_path, "r") as file:
            data = json.load(file)
        self.health = data[hero]["health"]
        self.max_health = data[hero]["health"]
        self.action = data[hero]["action"]
        self.abilities = data[hero]["abilities"]
        self.starting_space = data[hero]["starting space"]
        self.symbol = data[hero]["symbol"]

    def __str__(self):
        return f"Player(hero={self.hero}, health={self.health}, action={self.action}, abilities={self.abilities}, starting_space={self.starting_space}, hand={[str(card) for card in self.hand]})"
