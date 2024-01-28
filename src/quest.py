import json
import math


class Quest:
    def __init__(self, location, region, reward):
        self.reward = reward
        self.location = location
        json_file_path = "./data/questdata.json"
        with open(json_file_path, "r") as file:
            data = json.load(file)
        self.region = data[region][location]["region"]
        self.damage = data[region][location]["damage"]
        self.progression = data[region][location]["progression"]
        self.progress = 0

    def get_current_stage(self):
        return self.progression[self.progress]

    def q_action_card(self, player, card, lich_region):
        if card.type == self.progression[self.progress]:
            self.progress += 1
            player.health -= self.damage
            if lich_region == self.region:
                player.health -= 1

    def q_action_die(self, player, fdie, lich_region):
        self.progress += fdie
        player.health -= self.damage
        if lich_region == self.region:
            player.health -= 1

    def __str__(self):
        return f"Quest: Location - {self.location}, Region - {self.region}, Reward - {self.reward}, Damage - {self.damage}, Progression - {self.progression}, Progress - {self.progress}"

    def string_display(self, lich_region):
        prog = ""
        for x in range(self.progress, len(self.progression)):
            prog += self.progression[x][:1].upper()
        return f"{self.location}:\n{prog}\nDamage: {self.damage+1 if lich_region == self.region else self.damage}"

    def display_info(self, lich_region):
        prog = ""
        for x in range(self.progress, len(self.progression)):
            prog += self.progression[x][:1].upper()
        loc = self.location
        d = str(self.damage + 1 if lich_region == self.region else self.damage)
        num = 19  # max(len(loc), len(prog))
        loc = (
            (" " * math.ceil((num - len(loc)) // 2))
            + loc
            + (" " * math.ceil((num - len(loc)) // 2))
        )
        d = (" " * math.ceil((num - 1) // 2)) + d + (" " * math.ceil((num - 1) // 2))
        prog = (
            (" " * math.ceil((num - len(prog)) // 2))
            + prog
            + (" " * math.ceil((num - len(prog)) // 2))
        )
        return (loc, d, prog)
