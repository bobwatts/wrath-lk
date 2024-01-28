import sys
from roll import roll
import pathfind
from move_action import move_var_dist
from rest_action import rest
from flight_path_action import flight_path
from fight_action import fight
from quest_action import quest


def action_phase(
    current_player, players, locations, actions_left, quests, lich_region, hero_discard
):
    # actions_left = 4
    print(str(current_player.hero) + ": " + str(actions_left) + " actions left")
    strongholds = []
    for l in range(len(locations)):
        if current_player.symbol in locations[l].contents:
            location_ind = l
        if (
            "S" in locations[l].contents
            and current_player.symbol not in locations[l].contents
        ):
            strongholds.append(locations[l].name)
    possible_actions = ["Move"]
    # fight
    # remove this below############################################################################################################################################
    # locations[location_ind].contents.append("G")
    # locations[location_ind].contents.append("G")
    # locations[location_ind].contents.append("G")
    # locations[location_ind].contents.append("A")
    # end remove################################################################################################################################################
    if (
        "A" in locations[location_ind].contents
        or "G" in locations[location_ind].contents
    ):
        possible_actions.append("Fight")
    # quest or rest
    if "Q" in locations[location_ind].contents:
        possible_actions.append("Quest")
    else:
        possible_actions.append("Rest")
    if len(strongholds) > 0:
        possible_actions.append("Flight Path")
    travel2 = False
    travel4 = False
    heal = False
    for card in current_player.hand:
        if card.type == "TRAVEL":
            if card.strength == 2:
                travel2 = True
            else:
                travel4 = True
        if card.type == "HEAL":
            heal = True
    if travel2:
        possible_actions.append("Play Travel 2 Hero Card")
    if travel4:
        possible_actions.append("Play Travel 4 Hero Card")
    if heal:
        possible_actions.append("Play Heal Hero Card")
    # add character free actions here
    s = "Choose an action " + "(" + str(actions_left) + " left):\n"
    i = 1
    for a in possible_actions:
        s += "(" + str(i) + ") " + a + "\n"
        i += 1
    print(s)
    b = True
    while b:
        sys.stdout.write("->")
        try:
            choice = int(input())
            assert choice in range(1, i)
            b = False
        except:
            print("Invalid selection")
    if possible_actions[choice - 1] == "Move":
        actions_left -= 1
        locations = move_var_dist(
            current_player, players, location_ind, locations, 1, False
        )
    elif possible_actions[choice - 1] == "Fight":
        actions_left -= 1
        current_player, players, locations, hero_discard = fight(
            current_player, players, location_ind, locations, lich_region, hero_discard
        )
    elif possible_actions[choice - 1] == "Quest":
        actions_left -= 1
        current_player, players, quests, locations, hero_discard = quest(
            current_player,
            players,
            quests,
            locations,
            location_ind,
            lich_region,
            hero_discard,
        )
    elif possible_actions[choice - 1] == "Rest":
        actions_left -= 1
        current_player, players = rest(
            current_player, players, locations, False, location_ind
        )
    elif possible_actions[choice - 1] == "Flight Path":
        actions_left -= 1
        locations = flight_path(current_player, location_ind, locations, strongholds)
    elif possible_actions[choice - 1] == "Play Travel 2 Hero Card":
        locations = move_var_dist(
            current_player, players, location_ind, locations, 2, True
        )
        for card in range(len(current_player.hand)):
            if (
                current_player.hand[card].type == "TRAVEL"
                and current_player.hand[card].strength == 2
            ):
                hero_discard.append(current_player.hand.pop(card))
                break
    elif possible_actions[choice - 1] == "Play Travel 4 Hero Card":
        locations = move_var_dist(
            current_player, players, location_ind, locations, 4, True
        )
        for card in range(len(current_player.hand)):
            if (
                current_player.hand[card].type == "TRAVEL"
                and current_player.hand[card].strength == 4
            ):
                hero_discard.append(current_player.hand.pop(card))
                break
    elif possible_actions[choice - 1] == "Play Heal Hero Card":
        current_player, players = rest(
            current_player, players, locations, True, location_ind
        )
        for card in range(len(current_player.hand)):
            if (
                current_player.hand[card].type == "HEAL"
                and current_player.hand[card].strength == 1
            ):
                hero_discard.append(current_player.hand.pop(card))
                break
    return current_player, players, locations, quests, actions_left, hero_discard
