import sys
from roll import roll
import gameio

# def enemy_die(type, location_ind, locations):
#     for c in range(len(locations[location_ind].contents)):
#         if locations[location_ind].contents[c] == type:
#             locations
#             break


def fight(current_player, players, location_ind, locations, lich_region, hero_discard):
    roll_result = roll(2)
    attack = roll_result["attack"]
    defend = roll_result["defend"]
    ghouls = 0
    abominations = 0
    players_on_space_inds = []
    for i in range(len(locations[location_ind].contents)):
        if locations[location_ind].contents[i] == "G":
            ghouls += 1
        elif locations[location_ind].contents[i] == "A":
            abominations += 1
        else:
            for p in range(len(players)):
                if locations[location_ind].contents[i] == players[p].symbol:
                    players_on_space_inds.append(p)
    print(
        "You have "
        + str(ghouls)
        + " ghouls and "
        + str(abominations)
        + " abominations on your space. You rolled an attack of "
        + str(attack)
        + " and a defend of "
        + str(defend)
    )

    fighting = True
    # attack > 0 and (ghouls > 0 or abominations > 0) or if there are more attack cards to be used
    while fighting:
        enemies = ["Abomination"] * abominations + ["Ghoul"] * ghouls
        print("Deal " + str(attack) + " damage?")
        s = "Choose an enemy:\n"
        i = 1
        for a in enemies:
            s += "(" + str(i) + ") " + str(a) + "\n"
            i += 1
        target_cutoff = i
        print(s)
        play_attack = ""
        if len(players_on_space_inds) > 0:
            play_attack += "Or play attack card:\n"
            for p_a in players_on_space_inds:
                for card in range(len(players[p_a].hand)):
                    if players[p_a].hand[card].type == "ATTACK":
                        play_attack += (
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
                        # print(
                        #     "append to enemies: "
                        #     + str([p_a, players[p_a].hand[card].strength])
                        # )
                        enemies.append([p_a, players[p_a].hand[card].strength])
                        i += 1

            if play_attack == "Or play attack card:\n":
                play_attack = "(" + str(i) + ") " + "Quit"
            else:
                play_attack += "(" + str(i) + ") " + "Quit"
            enemies.append("Quit")
            i += 1
            print(play_attack)
        b = True
        while b:
            sys.stdout.write("->")
            try:
                choice = int(input())
                assert choice in range(1, i)
                b = False
            except:
                print("Invalid selection")
        # print("Choice = " + str(choice))
        if enemies[choice - 1] == "Quit":
            fighting = False
            break
        # elif choice <= target_cutoff:
        #     print("ENEMY SELECTED")
        elif enemies[choice - 1] == "Ghoul" and attack >= 1:
            attack -= 1
            enemies.remove("Ghoul")
            ghouls -= 1
            locations[location_ind].contents.remove("G")
            print("A ghoul was defeated!")
        elif enemies[choice - 1] == "Abomination" and attack >= 3:
            attack -= 3
            enemies.remove("Abomination")
            abominations -= 1
            locations[location_ind].contents.remove("A")
            print("The abomination was defeated!")
        elif enemies[choice - 1] == "Abomination" and attack < 3:
            print("Not enough damage to kill Abomination.")
        elif enemies[choice - 1] == "Ghoul" and attack < 1:
            print("Not enough damage to kill Ghoul.")

            # if ghoul then kill and damage - 1
            # if abomination then check for 3 damage. if 3 then kill if not check for ghouls and attack cards and if none then quit
            # check before if only an abomination, less than 3 attack damage and no attack cards (or maybe even not enough attack cards) and quit before
            # if do this be careful so code doesnt break when tirion's ability is added
        else:
            # print(enemies[choice - 1])
            p_choice = players[enemies[choice - 1][0]]
            cs_choice = enemies[choice - 1][1]
            for card in range(len(p_choice.hand)):
                if (
                    p_choice.hand[card].type == "ATTACK"
                    and p_choice.hand[card].strength == cs_choice
                ):
                    print(
                        "Played "
                        + p_choice.hero
                        + "'s ATTACK "
                        + str(cs_choice)
                        + " card"
                    )
                    hero_discard.append(p_choice.hand.pop(card))
                    attack += cs_choice
                    break
        all_enemies = True
        no_enemies = True
        for temp in enemies:
            if temp != "Ghoul" and temp != "Abomination":
                all_enemies == False
            else:
                no_enemies = False
        have_own_attack_card = False
        for card in current_player.hand:
            if card.type == "ATTACK":
                have_own_attack_card = True
        # if len(enemies) == 0:
        #     print("No more enemies")
        #     fighting = False
        if attack == 0 and all_enemies and not have_own_attack_card:
            fighting = False
            print("No more possible attacks.")
        elif no_enemies:
            fighting = False
            print("No more enemies.")
    hurt = 0
    for e in enemies:
        if e == "Ghoul" or e == "Abomination":
            hurt += 1
    if lich_region == locations[location_ind].region:
        print(
            "The Lich King exerts his baleful influence over the "
            + lich_region
            + " region!"
        )
    hurt -= defend
    hurt = max(hurt, 0)
    def_cards = 0
    for p in players_on_space_inds:
        for card in players[p].hand:
            if card.type == "DEFEND":
                def_cards += 1
    br = True
    while br:
        if def_cards > 0 and hurt > 0 and hurt > defend:
            hurt, br = gameio.defend_action_option(
                hurt, defend, current_player, players_on_space_inds, players
            )
        else:
            br = False
    print(current_player.hero + " takes " + str(hurt) + " damage!")
    current_player.health -= hurt
    return current_player, players, locations, hero_discard
