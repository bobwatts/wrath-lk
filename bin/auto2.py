import sys
import json

sys.path.append("./src")

import display
import load_game_data
import player
import spawn_ghouls
import pathfind
import gameio
import quest
import actions

board = load_game_data.starting_board()
hero_deck = load_game_data.create_hero_deck()
scourge_deck = load_game_data.create_scourge_deck()
scourge_discard = []
scourge = 0
despair = 0
json_file_path = "./data/constants.json"
with open(json_file_path, "r") as file:
    constants = json.load(file)
ghouls_left = constants["MAX_GHOULS"]
abominations_left = constants["MAX_ABOMINATIONS"]

# players = gameio.choose_players()
p1 = player.Player("Muradin Bronzebeard")
p2 = player.Player("Tirion Fordring")
players = [p1, p2]
########################################################################################
# gameio.place_players(board, players)
gameio.place_players_at_location(board, players, "Frosthold")
load_game_data.deal("Introductory", players)
from hero_card import HeroCard

# p1.hand.append(HeroCard("DEFEND_2"))
# p1.hand.append(HeroCard("DEFEND_2"))
# p1.hand.append(HeroCard("TRAVEL_2"))
# p2.hand.append(HeroCard("DEFEND_2"))
# p2.hand.append(HeroCard("DEFEND_2"))
# p2.hand.append(HeroCard("DEFEND_2"))

########################################################################################
# quests = load_game_data.set_up_random_quests(board)
quests = load_game_data.set_up_preset_quests(board)
# (
#     board,
#     scourge_deck,
#     scourge_discard,
#     ghouls_left,
#     abominations_left,
#     lich_region,
# ) = load_game_data.set_up_enemies(
#     board, scourge_deck, scourge_discard, ghouls_left, abominations_left
# )
lich_region = "green"

# argent tournament

for l in range(len(board)):
    if board[l].name == "Dalaran":
        board[l].contents.append("A")
        board[l].contents.append("A")
        abominations_left -= 1
display.display_with_lich(board, lich_region, False)

spawn_ghouls.activate_abominations(board, players, abominations_left, lich_region)

display.display_with_lich(board, lich_region, False)
