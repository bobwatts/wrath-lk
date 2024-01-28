class HeroCard:
    def __init__(self, name):
        #   "ATTACK_1": 5,
        #   "ATTACK_2": 5,
        #   "DEFEND_2": 5,
        #   "TRAVEL_2": 5,
        #   "TRAVEL_4": 5,
        #   "HEAL_1": 5,
        #   "STRONGHOLD": 3,
        #   "THE SCOURGE RISES": 8
        temp = name.split("_")
        if len(temp) == 1:
            if name == "THE SCOURGE RISES":
                self.type = "THE SCOURGE RISES"
                self.strength = None
            elif name == "STRONGHOLD":
                self.type = "STRONGHOLD"
                self.strength = None
            else:
                # print(name)
                self.type = name
                self.strength = -1
        else:
            self.type = temp[0]
            self.strength = int(temp[1])

    def __str__(self):
        return f"Type: {self.type}\Strength: {self.strength}"
