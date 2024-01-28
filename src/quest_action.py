# quest: show everyone's hands (that can contribute)
# option after roll: use attack (from dice),  name's ___ card, other name's __ card, etc
# continues until no attacks and there are no valid players with the appropriate card
# check if quest is deleted and if so, add reward card to player's hand (make sure to account for overflow hand)
# if hand is over 7 cards, call function (to be implemented) that allows players to discard down to 7 or play reward cards down to 7
# also implement reward cards (already done) but maybe with legends (descriptions that describe the card's effect)
# maybe add a free action to describe the function of a card in your hand?
import display
from roll import roll
import sys
import gameio


def quest(
    current_player, players, quests, locations, location_ind, lich_region, hero_discard
):
    for q in range(len(quests)):
        if quests[q].location == locations[location_ind].name:
            q_ind = q
    display.display_hands(players)
    roll_result = roll(2)
    attack = roll_result["attack"]
    defend = roll_result["defend"]
    display.display_quests_across(quests, lich_region)
    print("You rolled a " + str(attack) + " attack and a " + str(defend) + " defend!")
    contributing_players = []
    for i in range(len(locations[location_ind].contents)):
        for p in range(len(players)):
            if locations[location_ind].contents[i] == players[p].symbol:
                contributing_players.append(p)
    players_on_space_inds = []
    for i in range(len(locations[location_ind].contents)):
        for p in range(len(players)):
            if locations[location_ind].contents[i] == players[p].symbol:
                players_on_space_inds.append(p)
    # list cards in hand
    can_quest = True
    player_blacklist = {}
    while can_quest:
        if quests[q_ind].progress == len(quests[q_ind].progression):
            can_quest = False
            locations[location_ind].contents.remove("Q")
            print("Completed " + quests[q].location + "'s quest!")
            current_player.hand.append(quests[q_ind].reward)
            print(
                "Added "
                + str(quests[q_ind].reward.type)
                + " to "
                + current_player.hero
                + "'s hand!"
            )
            gameio.hand_overflow(current_player)
            if lich_region == quests[q].region:
                hurt = quests[q].damage + 1
            else:
                hurt = quests[q].damage
            # hurt -= defend
            # hurt = max(hurt, 0)
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
            can_quest = False
            quests.pop(q_ind)
            return current_player, players, quests, locations
        display.display_quests_across(quests, lich_region)
        print("")
        display.display_hands(players)
        # print("New option, could be possibilities")
        # print(quests[q_ind].get_current_stage())
        options_list = []
        i = 1
        if attack > 0:
            s = (
                "Choose a action to progress the quest:\n("
                + str(i)
                + ") Progress ("
                + str(attack)
                + " left)\n"
            )
            options_list.append("Progress Point")
            i += 1
        else:
            s = ""
        for p_a in contributing_players:
            for card in range(len(players[p_a].hand)):
                if players[p_a].hand[card].type == quests[
                    q_ind
                ].get_current_stage() and players[p_a].hero not in list(
                    player_blacklist.keys()
                ):
                    s += (
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
                    options_list.append([p_a, card])
                    i += 1
        if len(options_list) == 0 and attack == 0:
            print("No more possible actions")
            if lich_region == quests[q].region:
                print(
                    "The Lich King exerts his baleful influence over the "
                    + lich_region
                    + " region!"
                )
                hurt = quests[q].damage + 1
            else:
                hurt = quests[q].damage
            # hurt -= defend
            # hurt = max(hurt, 0)
            def_cards = 0
            for p in players_on_space_inds:
                for card in players[p].hand:
                    if card.type == "DEFEND":
                        def_cards += 1
            br = True
            while br:
                if def_cards > 0 and hurt > 0 and hurt > defend:
                    hurt, br = gameio.defend_action_option(
                        hurt,
                        defend,
                        current_player,
                        players_on_space_inds,
                        players,
                        hero_discard,
                    )
                else:
                    br = False
            print(current_player.hero + " takes " + str(hurt) + " damage!")
            current_player.health -= hurt
            can_quest = False
            return current_player, players, quests, locations
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
        if options_list[choice - 1] == "Progress Point":
            print("Progress Point Used!")
            attack -= 1
            quests[q].progress += 1
        else:
            print(
                "Advanced Quest Marker: "
                + str(players[options_list[choice - 1][0]].hero)
                + " contributed their "
                + str(
                    players[options_list[choice - 1][0]]
                    .hand[options_list[choice - 1][1]]
                    .type
                )
                + " "
                + str(
                    players[options_list[choice - 1][0]]
                    .hand[options_list[choice - 1][1]]
                    .strength
                )
            )
            quests[q].progress += 1
            # players[options_list[choice - 1][0]].hand.pop(options_list[choice - 1][1])
            player_blacklist[players[options_list[choice - 1][0]].hero] = 1
