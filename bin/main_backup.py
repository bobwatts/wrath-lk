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
from actions import action_phase

board = load_game_data.starting_board()
scourge_deck = load_game_data.create_scourge_deck()
scourge_discard = []
hero_discard = []
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
(
    locations,
    scourge_deck,
    discard,
    ghouls_left,
    abominations_left,
    lich_region,
) = load_game_data.set_up_enemies(
    board, scourge_deck, scourge_discard, ghouls_left, abominations_left
)

# display.display(board)
# display.display_with_lich(board, lich_region, True)
# display.display_quests_across(quests, "green")
# print()
# display.display_meters(scourge, despair)
# print()
# display.display_hands(players)

current_player_index = load_game_data.find_first_player_ind(players)
game_running = True
while game_running:
    if lich_region != "Icecrown Citadel":
        display.display_with_lich(board, lich_region, False)
        display.display_quests_across(quests, "green")
        print()
        display.display_meters(scourge, despair)
        print()
        display.display_hands(players)
    else:
        display.display_with_lich(board, lich_region, True)
        display.display_quests_across(quests, "green")
        print()
        display.display_meters(scourge, despair)
        print()
        display.display_hands(players)
    # actions
    actions_left = 4
    while actions_left > 0:
        (
            players[current_player_index],
            players,
            locations,
            quests,
            actions_left,
            hero_discard,
        ) = action_phase(
            players[current_player_index],
            players,
            board,
            actions_left,
            quests,
            lich_region,
            hero_discard,
        )
        if len(quests) == 0:
            # implement next phase
            board, quests, lich_region = gameio.unlock_citadel(board, quests)
        players, locations, despair, hero_discard = game_flow.check_for_deaths(
            players, locations, despair, hero_discard
        )
        if despair == constants["MAX_DESPAIR"]:
            game_running = False
            break
    if despair == constants["MAX_DESPAIR"]:
        break
    # draw two cards
    (
        current_player_index,
        players,
        hero_deck,
        hero_discard,
        scourge,
        scourge_deck,
        lich_region,
        ghouls_left,
        abominations_left,
        scourge_discard,
        despair,
    ) = gameio.draw_two(
        current_player_index,
        players,
        hero_deck,
        hero_discard,
        locations,
        scourge,
        scourge_deck,
        lich_region,
        ghouls_left,
        abominations_left,
        scourge_discard,
        despair,
    )
    # spawn ghouls
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
    # activate abominations
    (
        board,
        players,
        abominations_left,
        lich_region,
        hero_discard,
    ) = spawn_ghouls.activate_abominations(
        board, players, abominations_left, lich_region, hero_discard
    )
    players, locations, despair, hero_discard = game_flow.check_for_deaths(
        players, locations, despair, hero_discard
    )
    if despair == constants["MAX_DESPAIR"]:
        game_running = False
        break
    # next player
    current_player_index = game_flow.next_player_ind(current_player_index, players)

display.display_with_lich(board, lich_region, False)
display.display_quests_across(quests, "green")
print()
display.display_meters(scourge, despair)
print()
display.display_hands(players)

if despair == constants["MAX_DESPAIR"]:
    print("Despair has reached maximum.\nTry again.")
else:
    print("Congratulations, you beat the Lich King!")

# do turns starting with first player and itering through lsit from there
# do 4 actions and free actions
# draw 2 hero cards (check for overflow)
# run spawn ghouls
# run activate abomindations (check for deaths) finish method finally (add in opportunity to play defend cards)

# Notes: constantly check despair meter and exit (add in checks when changed)

# have all functions return game_running to end game if despair is maxed
# -- FINISH FUNCTION, LOTS TO IMPLEMENT

# can troubleshoot display contents if needed, might be faulty (could be hidden and not matter though)


# List:
# fix shuffling of piles in hero_deck at start
#
