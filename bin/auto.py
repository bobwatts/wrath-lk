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
# gameio.place_players(board, players)
gameio.place_players_at_location(board, players, "The Nexus")
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
lich_region = "red"
(
    scourge,
    scourge_deck,
    lich_region,
    ghouls_left,
    abominations_left,
    scourge_discard,
    board,
    despair,
) = spawn_ghouls.scourge_rises_action(
    scourge,
    scourge_deck,
    lich_region,
    ghouls_left,
    abominations_left,
    scourge_discard,
    board,
    despair,
)
# gameio.place_stronghold(board)
lich_region = "red"
display.display_with_lich(board, lich_region, False)
lich_region = "green"
display.display_with_lich(board, lich_region, False)
lich_region = "purple"
display.display_with_lich(board, lich_region, False)
display.display_quests_across(quests, lich_region)

from location import Location

board.append(Location("Icecrown Citadel", None, ["FILL IN LATER USING CONSTANTS"]))
lich_region = "Icecrown Citadel"
print("WASSUP")
display.print_board_contents(board)
display.display_with_lich(board, lich_region, True)
display.display_with_lich(board, lich_region, True)
display.print_board_contents(board)
# display.display_hands(players)
# load_game_data.deal("Introductory", players)#######
from hero_card import HeroCard

p1.hand.append(HeroCard("ATTACK_1"))
p1.hand.append(HeroCard("ATTACK_2"))
p1.hand.append(HeroCard("ATTACK_2"))
p1.hand.append(HeroCard("ATTACK_1"))
p1.hand.append(HeroCard("ATTACK_2"))
p1.hand.append(HeroCard("ATTACK_2"))
p1.hand.append(HeroCard("ATTACK_2"))
p2.hand.append(HeroCard("ATTACK_1"))
p2.hand.append(HeroCard("HEAL_1"))
p2.hand.append(HeroCard("ATTACK_2"))
quests[2].progress = 12
display.display_hands(players)
# display.print_board_contents(board)
# p1_index_location = 14
# p2_index_location = 12
# actions.move_var_dist(p1, players, p1_index_location, board, 6, True)
# actions.move_var_dist(p2, players, p2_index_location, board, 6, True)
actions_left = 4
p1, players, board, quests, actions_left = actions.action_phase(
    p1, players, board, actions_left, quests, lich_region
)
# display.display(board)
display.display_with_lich(board, lich_region, True)
display.display_quests_across(quests, lich_region)
display.display_hands(players)
# gameio.option_play_defend("Muradin Bronzebeard", players, board)
# hand overflow function gameio test
# display.display(board)
# print()
# display.display_meters(scourge, despair)
# print()
# load_game_data.deal("Introductory", players)
# display.display_hands(players)
# (
#     board,
#     scourge_deck,
#     scourge_discard,
#     scourge,
#     despair,
#     ghouls_left,
#     abominations_left,
# ) = spawn_ghouls.spawn_ghouls(
#     board,
#     scourge_deck,
#     scourge_discard,
#     scourge,
#     despair,
#     ghouls_left,
#     abominations_left,
# )
# (
#     board,
#     scourge_deck,
#     scourge_discard,
#     scourge,
#     despair,
#     ghouls_left,
#     abominations_left,
# ) = spawn_ghouls.spawn_ghouls(
#     board,
#     scourge_deck,
#     scourge_discard,
#     scourge,
#     despair,
#     ghouls_left,
#     abominations_left,
# )
# display.display(board)
# print(str(board[0]))
# board[0].contents = ["A"]
# board[7].contents = ["M"]
# board[1].contents = ["F"]
# print(str(board[0]))
# # display.print_board_contents(board)
# display.display(board)
# spawn_ghouls.activate_abominations(board, players, abominations_left)
# print(pathfind.find_all_players(board))
# path, dist = pathfind.dijkstra(board, board[0], board[7])
# print([str(i) for i in path])
# print(dist)


# for playing hero cards, should be a method that any function can call called broadcast that somethwhat pauses game and gives option to play a defend card
# (the other hero cards are used as free actions or only during fights)
# E.g. if defend cards in play: go Muradin is about to take {#} damage! Options: Muradin Defend 2: (1), Tirion Fordring Defend 2: (2), Nothing: (3)
