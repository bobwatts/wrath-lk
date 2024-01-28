import json
import player
import sys
from quest import Quest
from location import Location
import spawn_ghouls


def choose_players():
    json_file_path = "./data/constants.json"
    with open(json_file_path, "r") as file:
        constants = json.load(file)
    b = True
    while b:
        print("How many players (2-5)?")
        num_players = input()

        try:
            assert (
                int(num_players) >= constants["MIN_PLAYERS"]
                and int(num_players) <= constants["MAX_PLAYERS"]
            )
            b = False
        except:
            print("Not a number/Out of range")
    json_file_path = "./data/herodata.json"
    with open(json_file_path, "r") as file:
        heroes = json.load(file)
    heroes_list = list(heroes.keys())
    players = []
    for p in range(int(num_players)):
        b = True
        while b:
            print("Player " + str(p + 1) + " Hero:\n ")
            # m = 0
            for h in range(len(heroes_list)):
                print("(" + str(h + 1) + ") " + heroes_list[h])
                # m = h
            try:
                choice = int(input())
                print(choice)
                print(len(heroes_list))
                assert choice in range(1, len(heroes_list) + 1)
                b = False
            except:
                print("Not a valid choice")
        players.append(player.Player(heroes_list.pop(choice - 1)))
    return players


def place_players(locations, players):
    for p in players:
        for l in range(len(locations)):
            if locations[l].name == p.starting_space:
                locations[l].contents.append(p.symbol)
    return locations


def place_stronghold(locations):
    s = "Choose a location to place the stronghold:\n"
    m = 0
    choices = {}
    for l in range(len(locations)):
        if "Q" not in locations[l].contents and "S" not in locations[l].contents:
            if m % 3 == 0 or m % 3 == 1:
                e = " " * (27 - len(locations[l].name))
            else:
                e = "\n"
            s += "(" + str(m + 1) + ") " + locations[l].name + e
            choices[str(m + 1)] = locations[l].name
            m += 1
    print(s)
    b = True
    while b:
        try:
            sys.stdout.write("->")
            choice = int(input())
            assert choice in range(1, m + 2)
            for l in range(len(locations)):
                if locations[l].name == choices[str(choice)]:
                    locations[l].contents.append("S")
                    b = False
        except:
            print("Invalid choice")
    return locations


# could use this system of defending or simply write it into all possible sources of damage when damage is implemented
def defend_start(current_player_name, players):
    for p in range(len(players)):
        if players[p].name == current_player_name:
            return players[p].health
    assert False, "defend start misuse error"


def defend_end(current_player_name, players, saved_health):
    for p in range(len(players)):
        if players[p].name == current_player_name:
            if (players[p].health - saved_health) in range(0, 3):
                players[p].health = saved_health
            elif (players[p].health - saved_health) > 2:
                players[p].health += 2
            return players
    assert False, "defend end misuse error"


def option_play_defend(current_player_name, players, locations):
    json_file_path = "./data/herodata.json"
    with open(json_file_path, "r") as file:
        heroes = json.load(file)
    curr_symbol = heroes[current_player_name]["symbol"]
    symbols = {}
    for h in heroes:
        symbols[h] = heroes[h]["symbol"]

    # for p in range(len(players)):
    #     if player[p].name == current_player_name:
    #         current_player_ind = p
    for l in range(len(locations)):
        if curr_symbol in locations[l].contents:
            heroes_on_spot = [current_player_name]
            for c in locations[l].contents:
                if c in list(symbols.keys()):
                    for p in players:
                        for card in players[p].hand:
                            if card.type == "defend":
                                heroes_on_spot.append(symbols[c])
    s = "Would any of the following players want to play a defend card?\n"
    i = 1
    for h in heroes_on_spot:
        s += "(" + str(i) + ") " + h
    print(s)
    b = True
    while b:
        try:
            sys.stdout.write("->")
            choice = int(input())
            assert choice in range(1, len(heroes_on_spot) + 1)
            b = False
        except:
            print("Invalid Choice")
    # play defend


def defend_action_option(
    damage, defend, current_player, players_on_space_inds, players, hero_discard
):
    defend_choices = []
    def_string = (
        current_player.hero
        + " is about to take "
        + str(damage)
        + " damage with "
        + str(defend)
        + " defense! Play a defend card?\n"
    )
    i = 1
    for p_a in players_on_space_inds:
        for card in range(len(players[p_a].hand)):
            if players[p_a].hand[card].type == "DEFEND":
                def_string += (
                    "("
                    + str(i)
                    + ") "
                    + (
                        players[p_a].hero
                        + "'s "
                        + players[p_a].hand[card].type
                        + " "
                        + str(players[p_a].hand[card].strength)
                        + "\n"
                    )
                )
                defend_choices.append(p_a)
                i += 1
    def_string += "(" + str(i) + ") " + "Quit"
    if len(defend_choices) == 0:
        print("No defend cards to play")
        damage = max(damage - defend, 0)
        return damage, False
    defend_choices.append("Quit")
    i += 1
    print(def_string)
    b = True
    while b:
        sys.stdout.write("->")
        try:
            choice = int(input())
            assert choice in range(1, i)
            b = False
        except:
            print("Invalid selection")
    if choice == (i - 1):
        print("Quit received")
        damage = max(damage - defend, 0)
        return damage, False
    # print(choice - 1)
    # print(defend_choices[choice - 1])
    # print(players_on_space_inds[choice - 1])
    # DEBUG HERE IF NECESSARY
    # for i in players[players_on_space_inds[choice - 1]].hand:
    #     print(i.type)
    # print(str(players))
    # print(str(players_on_space_inds))
    # print(defend_choices)
    # print(str(defend_choices[choice - 1]))
    # print(str(players[defend_choices[choice - 1]]))
    # for card in players[defend_choices[choice - 1]].hand:
    # print(str(card))
    for card in range(len(players[defend_choices[choice - 1]].hand)):
        if players[defend_choices[choice - 1]].hand[card].type == "DEFEND":
            # print("Found card")
            hero_discard.append(players[defend_choices[choice - 1]].hand.pop(card))
            damage = max(damage - 2, 0)
            break
    # print("Fail if not found")
    damage = max(damage - defend, 0)
    return damage, True


def hand_overflow(current_player, hero_discard):
    json_file_path = "./data/constants.json"
    with open(json_file_path, "r") as file:
        constants = json.load(file)
    # if len(current_player.hand) > constants["HAND_LIMIT"]:
    while len(current_player.hand) > constants["HAND_LIMIT"]:
        s = (
            "Hand limit is "
            + str(constants["HAND_LIMIT"])
            + " cards. Discard or play reward cards until you are within the limit.\n"
            + current_player.hero
            + "'s Hand Size: "
            + str(len(current_player.hand))
            + "\n"
        )
        discard_choices = []
        i = 1
        for card in range(len(current_player.hand)):
            # print("here")
            # print(current_player.hand[card])
            if current_player.hand[card].strength == -1:
                s += "(" + str(i) + ") " + (current_player.hand[card].type + "\n")
            else:
                s += (
                    "("
                    + str(i)
                    + ") "
                    + (
                        current_player.hand[card].type
                        + " "
                        + str(current_player.hand[card].strength)
                        + "\n"
                    )
                )
            discard_choices.append(card)
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
        # if current_player.hand[choice - 1].type == "REWARD":
        if current_player.hand[choice - 1].strength == -1:
            response = "Played " + str(current_player.hand.pop(choice - 1).type) + "."
            # insert function call for reward card here
        else:
            hero_discard.append(current_player.hand.pop(choice - 1))
            response = (
                "Discarded "
                + str(hero_discard[-1].type)
                + " "
                + str(hero_discard[-1].strength)
                + "."
            )
        print(response)
    return current_player, hero_discard


def place_players_at_location(locations, players, location_name):
    for p in players:
        for l in range(len(locations)):
            if locations[l].name == location_name:
                locations[l].contents.append(p.symbol)
    return locations


def choose_difficulty():
    json_file_path = "./data/constants.json"
    with open(json_file_path, "r") as file:
        constants = json.load(file)
    difficulties = list(constants["DIFFICULTIES"].keys())
    b = True
    while b:
        print("Choose a difficulty:")
        for i in range(len(difficulties)):
            print("(" + str(i + 1) + ") " + difficulties[i])
        try:
            choice = int(input())
            assert choice in range(1, len(difficulties) + 1)
            b = False
        except:
            print("Not a valid choice")
    print("Chose " + difficulties[choice - 1] + " difficulty")
    return difficulties[choice - 1]


def draw_two(
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
):
    cards = [hero_deck.pop(0), hero_deck.pop(0)]
    for card in cards:
        if card.type == "STRONGHOLD":
            print("You drew a Stronghold card!")
            place_stronghold(locations)
        elif card.type == "THE SCOURGE RISES":
            # print("DESPAIR IS" + str(despair))
            print("The Scourge Rises!")

            (
                scourge,
                scourge_deck,
                lich_region,
                ghouls_left,
                abominations_left,
                scourge_discard,
                locations,
                despair,
            ) = spawn_ghouls.scourge_rises_action(
                scourge,
                scourge_deck,
                lich_region,
                ghouls_left,
                abominations_left,
                scourge_discard,
                locations,
                despair,
            )
            # print("DESPAIR IS" + str(despair))
        else:
            players[current_player_index].hand.append(card)
    # players[current_player_index].hand.append(hero_deck.pop(0))
    players[current_player_index], hero_discard = hand_overflow(
        players[current_player_index], hero_discard
    )
    return (
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
    )


def unlock_citadel(locations, quests):
    print(
        "Completed all three quests! Icecrown Citadel is now unlocked! IMPLEMENT THIS FUNCTION"
    )
    lich_region = "Icecrown Citadel"
    quests.append(Quest("Icecrown Citadel", "Icecrown Citadel", None))
    citadel = Location(
        "Icecrown Citadel" "Icecrown Citadel",
        ["The Breach", "Shadow Vault", "The Avalanche", "The Wrathgate"],
    )
    citadel.contents.insert(0, "Q")
    citadel.contents.insert(0, "K")
    locations.append(citadel)

    return (
        locations,
        quests,
        lich_region,
    )
