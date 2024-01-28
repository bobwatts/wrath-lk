import json
import random
import location
import hero_card
import math
from quest import Quest
from hero_card import HeroCard


def starting_board():
    json_file_path = "./data/mapdata.json"

    with open(json_file_path, "r") as file:
        locs = json.load(file)
    board = []
    for l in locs:
        board.append(location.Location(l, locs[l]["region"], locs[l]["neighbors"]))

    return board


def create_hero_deck():
    json_file_path = "./data/hero_deck.json"
    hd = []
    with open(json_file_path, "r") as file:
        temp = json.load(file)
    for k in temp:
        for _ in range(temp[k]):
            hd.append(k)

    scourge, stronghold, rest = [], [], []
    #   "ATTACK_1": 5,
    #   "ATTACK_2": 5,
    #   "DEFEND_2": 5,
    #   "TRAVEL_2": 5,
    #   "TRAVEL_4": 5,
    #   "HEAL_1": 5,
    #   "STRONGHOLD": 3,
    #   "THE SCOURGE RISES": 8
    for card in hd:
        uns_card = hero_card.HeroCard(card)
        if uns_card.type == "THE SCOURGE RISES":
            scourge.append(uns_card)
        elif uns_card.type == "STRONGHOLD":
            stronghold.append(uns_card)
        else:
            rest.append(uns_card)
    random.shuffle(rest)

    return scourge, stronghold, rest


def create_scourge_deck():
    json_file_path = "./data/mapdata.json"
    with open(json_file_path, "r") as file:
        board = json.load(file)
    temp = list(board.keys())
    random.shuffle(temp)
    return temp


def deal(difficulty, players):
    scourge_rises, strongholds, hero_deck = create_hero_deck()
    json_file_path = "./data/constants.json"
    with open(json_file_path, "r") as file:
        constants = json.load(file)
    for _ in range(constants["STARTING_HAND_SIZE"][str(len(players))]):
        for p in range(len(players)):
            players[p].hand.append(hero_deck.pop())
    piles = []
    num_piles = constants["DIFFICULTIES"][difficulty][0]
    for i in range(num_piles):
        piles.append([])
        piles[-1].append(scourge_rises.pop())
        if (
            i in range(constants["DIFFICULTIES"][difficulty][1])
            and difficulty != "Mythic"
        ):
            piles[-1].append(strongholds.pop())
        elif difficulty == "Mythic" and i == 1:
            piles[-1].append(strongholds.pop())
    while len(hero_deck) > 0:
        for p in range(num_piles):
            if len(hero_deck) > 0:
                piles[p].append(hero_deck.pop())
    result = []
    for s in piles:
        random.shuffle(s)
        result += s
    return result


def set_up_random_quests(locations):
    json_file_path = "./data/questdata.json"
    with open(json_file_path, "r") as file:
        qdata = json.load(file)
    json_file_path = "./data/reward_deck.json"
    with open(json_file_path, "r") as file:
        rdata = json.load(file)
        rdata = rdata["Reward Cards"]
        rkeys = list(rdata.keys())
    quests = []
    regs = ["red", "green", "purple"]
    for r in regs:
        klist = list(qdata[r].keys())
        random.shuffle(klist)
        random.shuffle(rkeys)
        reward = rkeys.pop(0)
        quests.append(
            Quest(klist.pop(0), r, HeroCard(reward))
        )  ##(reward, rdata[reward])))
        for l in range(len(locations)):
            if locations[l].name == quests[-1].location:
                locations[l].contents.append("Q")
    return quests


def set_up_enemies(locations, scourge, discard, ghouls_left, abominations_left):
    random.shuffle(scourge)
    first = scourge.pop()
    second = scourge.pop()
    two = [scourge.pop(), scourge.pop(), scourge.pop()]
    one = [scourge.pop(), scourge.pop(), scourge.pop()]
    ab = scourge.pop()
    for l in range(len(locations)):
        if locations[l].name == first:
            for _ in range(3):
                ghouls_left -= 1
                locations[l].contents.append("G")
            lich_region = locations[l].region
        elif locations[l].name == second:
            for _ in range(3):
                ghouls_left -= 1
                locations[l].contents.append("G")
        elif locations[l].name == ab:
            abominations_left -= 1
            locations[l].contents.append("A")
        for o in one:
            if o == locations[l].name:
                ghouls_left -= 1
                locations[l].contents.append("G")
                break
        for t in two:
            if t == locations[l].name:
                for _ in range(2):
                    ghouls_left -= 1
                    locations[l].contents.append("G")
                break
    discard.append(first)
    discard.append(second)
    discard.extend(two)
    discard.extend(one)
    discard.append(ab)
    return locations, scourge, discard, ghouls_left, abominations_left, lich_region


def set_up_preset_quests(locations):
    json_file_path = "./data/questdata.json"
    with open(json_file_path, "r") as file:
        qdata = json.load(file)
    json_file_path = "./data/reward_deck.json"
    with open(json_file_path, "r") as file:
        rdata = json.load(file)
        rdata = rdata["Reward Cards"]
        rkeys = list(rdata.keys())
    preset_rewards = ["Argent Crusaders", "Borrowed Time", "One Quiet Night"]
    random.shuffle(preset_rewards)
    quests = []
    quests.append(
        Quest(
            "Naxxramas", "purple", HeroCard(preset_rewards[0])
        )  # (preset_rewards[0], rdata[preset_rewards[0]])
    )
    quests.append(
        Quest(
            "Ulduar", "green", HeroCard(preset_rewards[1])
        )  # (preset_rewards[1], rdata[preset_rewards[1]]))
    )
    quests.append(
        Quest(
            "The Nexus", "red", HeroCard(preset_rewards[2])
        )  # (preset_rewards[2], rdata[preset_rewards[2]]))
    )
    for l in range(len(locations)):
        for q in range(3):
            if locations[l].name == quests[q].location:
                locations[l].contents.append("Q")
    return quests


def find_first_player_ind(players):
    json_file_path = "./data/hero_starts.json"
    with open(json_file_path, "r") as file:
        start_data = json.load(file)
    northmost = 0
    for p in range(len(players)):
        if (
            start_data["NORTH_RANKINGS"][players[p].starting_space]
            > start_data["NORTH_RANKINGS"][players[northmost].starting_space]
        ):
            northmost = p
    return northmost
