import sys


def flight_path(player, location_ind, locations, strongholds):
    locations[location_ind].contents.remove(player.symbol)
    if len(strongholds) == 1:
        choice = 1
    else:
        print("Which stronghold would you like to travel to?")
        s = "Choose a stronghold\n"
        i = 1
        for a in strongholds:
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
    for l in range(len(locations)):
        if locations[l].name == strongholds[choice - 1]:
            # print("here")
            # print(locations[l].name)
            locations[l].contents.append(player.symbol)
            # print(locations[l].contents)
            print(
                player.hero + " flies to the stronghold at " + locations[l].name + "!"
            )
    return locations
