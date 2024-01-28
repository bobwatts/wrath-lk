import json

import load_game_data
import print_board
import print_board_lich
import print_board_lich_icecrown


class Colors:
    RESET = "\033[0m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"


# print(Colors.RED + Colors.BG_YELLOW + "Red text on yellow background" + Colors.RESET)
# print(Colors.GREEN + Colors.BG_BLUE + "Green text on blue background" + Colors.RESET)
# print(Colors.WHITE + Colors.BG_MAGENTA + "White text on magenta background" + Colors.RESET)


def print_board_contents(board):
    for l in board:
        print(str(l) + "\n\n")


def display(locations):
    k = {}
    for l in locations:
        if l.quest:
            temp = l.contents
            for v in range(8):
                try:
                    if temp[v] == "0":
                        pass
                        # print("error")
                except:
                    temp.append("0")
            temp.push("Q")
            k[l.name] = temp
        else:
            temp = l.contents
            for v in range(9):
                try:
                    if temp[v] == "0":
                        pass
                        # print("error")
                except:
                    temp.append("0")
            k[l.name] = temp
    with open("./data/display_full.txt", "r") as file:
        content = file.read()
        print_board.print_map(content, k)
    for l in range(len(locations)):
        b = True
        while b:
            try:
                locations[l].contents.remove("0")
            except:
                b = False


def display_hands(players):
    dis = ""
    for p in players:
        dis += (
            "|"
            + (" " * (14 - len(p.hero) // 2))
            + p.hero
            + " ("
            + str(p.health)
            + ")"
            + (" " * (14 - len(p.hero) // 2))
        )
    dis += "|\n"
    max_hand = max([len(p.hand) for p in players])
    for i in range(max_hand):
        for p in players:
            if i < len(p.hand):
                if p.hand[i].strength == -1:
                    dis += (
                        "|"
                        + (" " * (16 - len(p.hand[i].type) // 2))
                        + p.hand[i].type
                        + (" " * (16 - len(p.hand[i].type) // 2))
                    )
                else:
                    dis += (
                        "|"
                        + (" " * (16 - len(p.hand[i].type) // 2))
                        + p.hand[i].type
                        + " "
                        + str(p.hand[i].strength)
                        + (" " * (15 - len(p.hand[i].type) // 2))
                    )
            else:
                dis += "|" + (" " * 33)
        dis += "|\n"
    print(dis)


def display_meters(scourge, despair):
    print("Scourge Track: " + "| " * (scourge) + "|S" + "| " * (8 - scourge) + "|")
    print("               |2|2|3|3|3|4|4|4|5|\n")
    print("Despair Track: " + "| " * (despair) + "|X" + "| " * (9 - despair) + "|")


def display_quests(quests, lich_region):
    for q in quests:
        print(q.string_display(lich_region))


def display_quests_across(quests, lich_region):
    s = ""
    for q in quests:
        temp, _, _ = q.display_info(lich_region)
        s = s + temp + "   |   "
    s += "\n"
    for q in quests:
        _, temp, _ = q.display_info(lich_region)
        s = s + str(temp) + "   |   "
    s += "\n"
    for q in quests:
        _, _, temp = q.display_info(lich_region)
        s = s + temp + "   |   "
    print(s)


def display_with_lich(locations, lich_region, icecrown):
    k = {}
    for l in locations:
        if l.name == "Icecrown Citadel":
            # print("Yo")
            temp = l.contents
            for v in range(12):
                try:
                    if temp[v] == "0":
                        pass
                        # print("error")
                except:
                    temp.append("0")
            # temp.insert(0, "Q")
            # temp.insert(0, "K")
            # temp.append("Q")
            # temp.append("K")
            k[l.name] = temp
        else:
            if l.quest:
                temp = l.contents
                for v in range(8):
                    try:
                        if temp[v] == "0":
                            pass
                            # print("error")
                    except:
                        temp.append("0")
                # temp.push("Q")
                temp.insert(0, "Q")
                k[l.name] = temp
            else:
                temp = l.contents
                for v in range(9):
                    try:
                        if temp[v] == "0":
                            pass
                            # print("error")
                    except:
                        temp.append("0")
                k[l.name] = temp
    json_file_path = "./data/constants.json"
    with open(json_file_path, "r") as file:
        constants = json.load(file)
    empty_marker = ["             "] * 13
    if lich_region == "red":
        k["Red Lich"] = constants["LICH_SYMBOL"]
        k["Green Lich"] = empty_marker
        k["Purple Lich"] = empty_marker
    elif lich_region == "green":
        k["Red Lich"] = empty_marker
        k["Green Lich"] = constants["LICH_SYMBOL"]
        k["Purple Lich"] = empty_marker
    elif lich_region == "purple":
        k["Red Lich"] = empty_marker
        k["Green Lich"] = empty_marker
        k["Purple Lich"] = constants["LICH_SYMBOL"]
    else:
        k["Red Lich"] = empty_marker
        k["Green Lich"] = empty_marker
        k["Purple Lich"] = empty_marker
    if not icecrown:
        with open("./data/board_lich_display_lock.txt", "r") as file:
            content = file.read()
            print_board_lich.print_map(content, k)
    else:
        with open("./data/board_lich_display_unlock.txt", "r") as file:
            content = file.read()
            print_board_lich_icecrown.print_map(content, k)
    for l in range(len(locations)):
        b = True
        while b:
            displays = []
            try:
                locations[l].contents.remove("0")
            except:
                b = False
                # displays.append(False)
            # try:
            #     locations[l].contents.remove("Q")
            # except:
            #     # b = False
            #     displays.append(False)
            # try:
            #     locations[l].contents.remove("K")
            # except:
            #     # b = False
            #     displays.append(False)
