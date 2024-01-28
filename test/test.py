import sys

sys.path.append("./src")

import display
import load_game_data
import player

board = load_game_data.starting_board()
# hero_deck = load_game_data.create_hero_deck()
# scourge_deck = load_game_data.create_scourge_deck()

p1 = player.Player("Muradin Bronzebeard")
p2 = player.Player("Tirion Fordring")
players = [p1, p2]


display.display(board)
print()
display.display_meters(1, 1)
print()
load_game_data.deal("Introductory", players)
display.display_hands(players)
