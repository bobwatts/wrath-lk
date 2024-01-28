from roll import roll
import sys


def rest(player, players, locations, from_card, location_ind):
    num = roll(2)["attack"]
    if "S" in locations[location_ind].contents:
        print("+1 Heal from the Stronghold!")
        num += 1
    if from_card:
        targets = []
        for l in range(len(locations)):
            if player.symbol in locations[l].contents:
                for i in range(len(locations[l].contents)):
                    for p in range(len(players)):
                        if players[p].symbol == locations[l].contents[i]:
                            targets.append(p)
        if len(targets) == 1:
            players[targets[0]].health += num + 1
            print(players[targets[0]].hero + " heals for " + str(num + 1) + "!")
        else:
            print("Who do you want to heal?")
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
                    choice = int(input())
                    assert choice in range(1, i)
                    b = False
                except:
                    print("Invalid selection")
            players[targets[choice - 1]].health += num + 1
            print(
                players[targets[choice - 1]].hero + " heals for " + str(num + 1) + "!"
            )
            if (
                players[targets[choice - 1]].health
                >= players[targets[choice - 1]].max_health
            ):
                players[targets[choice - 1]].health = players[
                    targets[choice - 1]
                ].max_health
                print(players[targets[choice - 1]].hero + " is now at full health!")
    else:
        player.health += num
        print(player.hero + " heals for " + str(num) + "!")
        if player.health >= player.max_health:
            player.health = player.max_health
            print(player.hero + " is now at full health!")
    return player, players
