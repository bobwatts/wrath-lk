import json
import random
import pathfind
import sys
import gameio


# replace all appends with this
def add_ghoul(locations, name, ghouls_left, despair):
    if ghouls_left > 0:
        locations[name].contents.insert(0, "G")
        ghouls_left -= 1
    else:
        print("Out of Ghouls. Despair is advanced by 1")
        despair += 1
    return locations, name, ghouls_left, despair


# and this
def add_abomination(locations, name, abominations_left, despair):
    if abominations_left > 0:
        locations[name].contents.insert(0, "A")
        abominations_left -= 1
    else:
        print("Out of Abominations. Despair is advanced by 1")
        despair += 1
    return locations, name, abominations_left, despair


def spawn_ghouls(
    locations,
    scourge_deck,
    scourge_discard,
    scourge,
    despair,
    ghouls_left,
    abominations_left,
):
    json_file_path = "./data/constants.json"
    with open(json_file_path, "r") as file:
        constants = json.load(file)
    num_cards = constants["SCOURGE"][scourge]
    for _ in range(num_cards):
        if len(scourge_deck) == 0:
            random.shuffle(scourge_discard)
            scourge_deck = scourge_discard
            scourge_discard = []
        scourge_discard.append(scourge_deck.pop())
        for l in range(len(locations)):
            if locations[l].name == scourge_discard[-1]:
                if ghouls_left == 0:
                    despair += 1
                else:
                    if locations[l].contents.count("G") == 3:
                        # locations[l].contents.insert(0, "A")
                        # abominations_left -= 1
                        # despair += 1
                        add_abomination(locations, l, abominations_left, despair)
                    else:
                        # locations[l].contents.insert(0, "G")
                        # ghouls_left -= 1
                        add_ghoul(locations, l, ghouls_left, despair)
    return (
        locations,
        scourge_deck,
        scourge_discard,
        scourge,
        despair,
        ghouls_left,
        abominations_left,
    )


def find_keys_with_lowest_duplicate_values(dictionary):
    value_to_keys = {}
    lowest_value = float("inf")
    keys_with_lowest_value = []

    for key, value in dictionary.items():
        if value not in value_to_keys:
            value_to_keys[value] = [key]
        else:
            value_to_keys[value].append(key)

        if value < lowest_value:
            lowest_value = value
            keys_with_lowest_value = [key]
        elif value == lowest_value:
            keys_with_lowest_value.append(key)

    # Filter out only the keys with lowest values that have duplicates
    result_keys = list(
        set(keys_with_lowest_value)
        & set(key for key_list in value_to_keys.values() if len(key_list) > 1)
    )

    return result_keys


# Example Usage
# example_dict = {'a': 3, 'b': 2, 'c': 3, 'd': 4, 'e': 2, 'f': 5}
# result = find_keys_with_lowest_duplicate_values(example_dict)
# print(result)


def activate_abominations(
    locations, players, abominations_left, lich_region, hero_discard
):
    # print("not completed yet")
    player_symbols = []
    player_locations_inds = {}
    for p in players:
        player_symbols.append(p.symbol)
        for l in range(len(locations)):
            if p.symbol in locations[l].contents:
                player_locations_inds[p.hero] = l
    ab_locations_ind = []
    for l in range(len(locations)):
        if locations[l].contents.count("A") > 0:
            for c in locations[l].contents:
                if c == "A":
                    ab_locations_ind.append(l)
    # print(ab_locations)
    # print(pathfind.find_nearest_player(locations, ab_locations[0]))
    # print(pathfind.find_distances_to_all_players(locations, ab_locations))
    for a in ab_locations_ind:
        player_on_square = False
        for x in locations[a].contents:
            if x in player_symbols:
                player_on_square = True
        # see if hero on current space, if yes then dont move (skip this part)
        if not player_on_square:
            player_distances = {}
            for p in players:
                player_distances[p.hero] = pathfind.dijkstra(
                    locations, locations[a], locations[player_locations_inds[p.hero]]
                )
            # print(player_distances)
            min_dist = 100
            targets = []
            for pd in player_distances:
                if player_distances[pd][1] < min_dist:
                    min_dist = player_distances[pd][1]
                    targets = [pd]
                elif player_distances[pd][1] == min_dist:
                    targets.append(pd)
            # run dijstra's algorithm on the player locations separetly
            # prompt player
            if len(targets) > 1:
                i = 1
                s = (
                    "Which hero should the abomination on "
                    + str(locations[a].name)
                    + " track?\n"
                )
                for t in targets:
                    s += (
                        "("
                        + str(i)
                        + ") "
                        + t
                        + " in "
                        + str(locations[player_locations_inds[t]].name)
                        + "\n"
                    )
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
            else:
                choice = 1
            locations[a].contents.remove("A")
            for l in range(len(locations)):
                if locations[l].name == player_distances[targets[choice - 1]][0][1]:
                    locations[l].contents.append("A")

            # print("not implemented")
    new_ab_locations_ind = []
    for l in range(len(locations)):
        if locations[l].contents.count("A") > 0:
            for c in locations[l].contents:
                if c == "A":
                    new_ab_locations_ind.append(l)
    for a in new_ab_locations_ind:
        players_on_square_ind = []
        for x in locations[a].contents:
            for p in range(len(players)):
                if players[p].symbol == x:
                    players_on_square_ind.append(p)
        if len(players_on_square_ind) == 1:
            print(
                "An abomination attacks "
                + str(players[players_on_square_ind[0]].hero + ".")
            )
            damage = locations[a].contents.count("A")
            if lich_region == locations[a].region:
                print(
                    "The Lich King exerts his baleful influence over the "
                    + lich_region
                    + " region!"
                )
                damage += 1
            # damage, blocked = gameio.defend_action_option(
            #     damage,
            #     0,
            #     players[players_on_square_ind[0]],
            #     players_on_square_ind,
            #     players,
            # )
            def_cards = 0
            for p in players_on_square_ind:
                for card in players[p].hand:
                    if card.type == "DEFEND":
                        def_cards += 1
            br = True
            while br:
                if def_cards > 0 and damage > 0:
                    # print(choice)
                    # print(players_on_square_ind)
                    damage, br = gameio.defend_action_option(
                        damage,
                        0,
                        players[choice - 1],
                        players_on_square_ind,
                        players,
                        hero_discard,
                    )
                elif damage <= 0:
                    br = False
                    print("Damage resolved.")
                else:
                    br = False
                    print("No more defend cards.")
            players[players_on_square_ind[0]].health -= damage
            print(
                players[players_on_square_ind[0]].hero
                + " takes "
                + str(damage)
                + " damage!"
            )
            # lich region
            # could be one or more abominations, damage is simultaneous
            # defend option
            # abomination attacks player
            # despair check
        elif locations[a].contents.count("A") == 1 and len(players_on_square_ind) > 1:
            # damage = locations[a].contents.count("A")
            damage = 1
            if lich_region == locations[a].region:
                damage += 1
            s = (
                "An Abomination is attacking for "
                + str(damage)
                + " damage in "
                + str(locations[a].name)
                + "!\nChoose who it attacks:\n"
            )
            i = 1
            for p in players_on_square_ind:
                s += "(" + str(i) + ") " + players[p].hero + "\n"
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
            def_cards = 0
            for p in players_on_square_ind:
                for card in players[p].hand:
                    if card.type == "DEFEND":
                        def_cards += 1
            br = True
            # tirion
            # muradin
            # choose tirion card()only one
            while br:
                # print(damage)
                if def_cards > 0 and damage > 0:
                    print(
                        "damage: "
                        + str(damage)
                        + "current player"
                        + str(players[choice - 1])
                        + "players on square"
                        + str(players_on_square_ind)
                    )
                    damage, br = gameio.defend_action_option(
                        damage,
                        0,
                        players[choice - 1],
                        players_on_square_ind,
                        players,
                        hero_discard,
                    )
                elif damage <= 0:
                    br = False
                    print("Damage resolved.")
                else:
                    br = False
                    print("No more defend cards.")
            print(
                players[players_on_square_ind[choice - 1]].hero
                + " takes "
                + str(damage)
                + " damage!"
            )
            # damage, blocked = gameio.defend_action_option(damage, 0, players[players_on_square_ind[choice-1]], players_on_square_ind, players)
            players[players_on_square_ind[choice - 1]].health -= damage
            # print(players[players_on_square_ind[choice-1].hero] + " takes " + str(damage) + " damage!")
            # lich check
            # choose which player the abomination attacks
            # defend option
            # abomination attacks chosen player
            # despair check
        elif locations[a].contents.count("A") > 1 and len(players_on_square_ind) > 1:
            num_ab = locations[a].contents.count("A")
            damage = 1
            if lich_region == locations[a].region:
                damage += 1
            print(
                "There are "
                + str(num_ab)
                + " abominations on "
                + str(locations[a].name)
                + "!\n"
            )
            abominations_attacking_targets = {}
            s = (
                "An Abomination is attacking for "
                + str(damage)
                + " damage in "
                + str(locations[a].name)
                + "!\nChoose who it attacks:\n"
            )
            i = 1
            for p in players_on_square_ind:
                s += "(" + str(i) + ") " + players[p].hero + "\n"
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
            # for p_a in players_on_square_ind:
            #     if players[p_a] not in list(abominations_attacking_targets.keys()):
            #         players[p_a] += 1
            #     else:
            #         players[p_a] = 1
            if players_on_square_ind[choice - 1] not in list(
                abominations_attacking_targets.keys()
            ):
                abominations_attacking_targets[players_on_square_ind[choice - 1]] = 1
            else:
                abominations_attacking_targets[players_on_square_ind[choice - 1]] += 1
            ################################################################
            for t in list(abominations_attacking_targets.keys()):
                current_damage = damage * abominations_attacking_targets[t]
                def_cards = 0
                for p in players_on_square_ind:
                    for card in players[p].hand:
                        if card.type == "DEFEND":
                            def_cards += 1
                br = True
                while br:
                    if def_cards > 0 and current_damage > 0:
                        current_damage, br = gameio.defend_action_option(
                            current_damage,
                            0,
                            players[choice - 1],
                            players_on_square_ind,
                            players,
                            hero_discard,
                        )
                    elif current_damage <= 0:
                        br = False
                        print("Damage resolved.")
                    else:
                        br = False
                        print("No more defend cards.")

                print(players[t].hero + " takes " + str(current_damage) + " damage!")
                players[t].health -= current_damage
    return locations, players, abominations_left, lich_region, hero_discard
    # lich check
    # go through each abomination and have players choose which player/s will be damaged
    # iterate through players getting damaged by 1 or more abominations and ask about defends
    # defend options for each player
    # abominations attacks chosen player/s

    # once all abomindations have moved:
    # check for lich_region in each case
    # if 1 abomindaation and 1 player, ask for defense then do damage
    # if multiple abominations and 1 player, ask for defense then do damage
    # if 1 abomination and multiple players, ask for target then ask for defense then do damage
    # if multiple abominations and multiple players, then:
    # ask for targets (separetlye for each abomination)
    # go through targets and ask for defense (group up attack if on same player, maybe add to dictionary?)
    # deal damage


def scourge_rises_action(
    scourge,
    scourge_deck,
    lich_region,
    ghouls_left,
    abominations_left,
    scourge_discard,
    locations,
    despair,
):
    scourge += 1
    card = scourge_deck.pop(0)
    for l in range(len(locations)):
        if locations[l].name == card:
            lich_region = locations[l].region
            while locations[l].contents.count("G") < 3:
                # locations[l].contents.append("G")
                locations, name, ghouls_left, despair = add_ghoul(
                    locations, l, ghouls_left, despair
                )
                ghouls_left -= 1
            # locations[l].contents.append("A")
            locations, name, abominations_left, despair = add_abomination(
                locations, l, ghouls_left, despair
            )
            break

    random.shuffle(scourge_discard)
    scourge_deck.extend(scourge_discard)
    scourge_discard = []
    return (
        scourge,
        scourge_deck,
        lich_region,
        ghouls_left,
        abominations_left,
        scourge_discard,
        locations,
        despair,
    )


# scourge,
#             scourge_deck,
#             lich_region,
#             ghouls_left,
#             abominations_left,
#             scourge_discard,
#             locations,
#             despair
