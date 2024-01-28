import sys

sys.path.append("./src")

import load_game_data
import display
import load_game_data
import json


locations = load_game_data.starting_board()
# test code for special characters
json_file_path = "./data/mapdata.json"
with open(json_file_path, "r") as file:
    data = json.load(file)
for l in range(len(locations)):
    for _ in range(9):
        locations[l].contents.append(data[locations[l].name]["spec"])
display.display(locations)
