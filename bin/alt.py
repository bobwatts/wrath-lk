import sys
import json

sys.path.append("./src")

import display
import load_game_data
import player
import spawn_ghouls
import pathfind

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
p1 = player.Player("Muradin Bronzebeard")
p2 = player.Player("Tirion Fordring")
players = [p1, p2]
# t_quest = quest.Quest("Naxxramas", "Whoopie Cushion")
# print(t_quest.string_display("purple"))
# p1 = player.Player("Muradin Bronzebeard")
# p2 = player.Player("Tirion Fordring")
# players = [p1, p2]

display.display(board)
print()
display.display_meters(scourge, despair)
print()
load_game_data.deal("Introductory", players)
display.display_hands(players)
(
    board,
    scourge_deck,
    scourge_discard,
    scourge,
    despair,
    ghouls_left,
    abominations_left,
) = spawn_ghouls.spawn_ghouls(
    board,
    scourge_deck,
    scourge_discard,
    scourge,
    despair,
    ghouls_left,
    abominations_left,
)
(
    board,
    scourge_deck,
    scourge_discard,
    scourge,
    despair,
    ghouls_left,
    abominations_left,
) = spawn_ghouls.spawn_ghouls(
    board,
    scourge_deck,
    scourge_discard,
    scourge,
    despair,
    ghouls_left,
    abominations_left,
)
display.display(board)
print(str(board[0]))
board[0].contents = ["A"]
board[7].contents = ["M"]
board[1].contents = ["F"]
print(str(board[0]))
# display.print_board_contents(board)
display.display(board)
spawn_ghouls.activate_abominations(board, players, abominations_left)
print(pathfind.find_all_players(board))
path, dist = pathfind.dijkstra(board, board[0], board[7])
print([str(i) for i in path])
print(dist)


# for playing hero cards, should be a method that any function can call called broadcast that somethwhat pauses game and gives option to play a defend card
# (the other hero cards are used as free actions or only during fights)
# E.g. if defend cards in play: go Muradin is about to take {#} damage! Options: Muradin Defend 2: (1), Tirion Fordring Defend 2: (2), Nothing: (3)


#################################################

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

players = gameio.choose_players()
gameio.place_players(board, players)
quests = load_game_data.set_up_random_quests(board)
display.display(board)
display.display_quests_across(quests, "green")

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
import game_flow

board = load_game_data.starting_board()
scourge_deck = load_game_data.create_scourge_deck()
scourge_discard = []
scourge = 0
despair = 0
json_file_path = "./data/constants.json"
with open(json_file_path, "r") as file:
    constants = json.load(file)
ghouls_left = constants["MAX_GHOULS"]
abominations_left = constants["MAX_ABOMINATIONS"]

players = gameio.choose_players()
difficulty = gameio.choose_difficulty()
hero_deck = load_game_data.deal(difficulty, players)

gameio.place_players(board, players)
quests = load_game_data.set_up_random_quests(board)


display.display(board)
display.display_quests_across(quests, "green")
print()
display.display_meters(scourge, despair)
print()
display.display_hands(players)

current_player_index = load_game_data.find_first_player_ind(players)
game_running = True
while game_running:
    current_player_index = game_flow.next_player_ind(current_player_index, players)


# starting player is northmost player (put rankings in hero_starts)
# do turns starting with first player and itering through lsit from there
# do 4 actions and free actions
# draw 2 hero cards (check for overflow)
# run spawn ghouls
# run activate abomindations (check for deaths) finish method finally (add in opportunity to play defend cards)

# Notes: constantly check despair meter


#
#
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


#
#

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
