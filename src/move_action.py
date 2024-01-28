import pathfind
import sys


def move_var_dist(player, players, current_location_ind, locations, dist, from_card):
    choices = pathfind.find_all_locations_in_radius(
        current_location_ind, locations, dist
    )
    if from_card:
        # in the future versions (for different devices), need to get the okay from the other player
        targets = []
        for l in range(len(locations)):
            if player.symbol in locations[l].contents:
                for i in range(len(locations[l].contents)):
                    for p in range(len(players)):
                        if players[p].symbol == locations[l].contents[i]:
                            targets.append(p)
        if len(targets) == 1:
            print("Where do you want to travel to?")
            s = "Choose a locations:\n"
            i = 1
            for a in choices:
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
            locations[current_location_ind].contents.remove(player.symbol)
            for l in range(len(locations)):
                if locations[l].name == choices[choice - 1]:
                    locations[l].contents.append(player.symbol)
            return locations
        else:
            print("Who do you want to move?")
            s = "Choose a hero:\n"
            i = 1
            for a in targets:
                s += "(" + str(i) + ") " + players[a].hero + "\n"
                i += 1
            print(s)
            b = True
            while b:
                sys.stdout.write("->")
                try:
                    choice_h = int(input())
                    assert choice_h in range(1, i)
                    b = False
                except:
                    print("Invalid selection")
                    print("Where do you want to travel to?")
            s = "Choose a locations:\n"
            i = 1
            for a in choices:
                s += "(" + str(i) + ") " + a + "\n"
                i += 1
            print(s)
            b = True
            while b:
                sys.stdout.write("->")
                try:
                    choice_l = int(input())
                    assert choice_l in range(1, i)
                    b = False
                except:
                    print("Invalid selection")
            locations[current_location_ind].contents.remove(
                players[targets[choice_h - 1]].symbol
            )
            for l in range(len(locations)):
                if locations[l].name == choices[choice_l - 1]:
                    locations[l].contents.append(players[targets[choice_h - 1]].symbol)
            return locations
    else:
        print("Where do you want to travel to?")
        s = "Choose a locations:\n"
        i = 1
        for a in choices:
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
        locations[current_location_ind].contents.remove(player.symbol)
        for l in range(len(locations)):
            if locations[l].name == choices[choice - 1]:
                locations[l].contents.append(player.symbol)
        return locations
