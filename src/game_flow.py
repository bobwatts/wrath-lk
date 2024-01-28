def next_player_ind(p, players):
    if p == len(players) - 1:
        p = 0
    else:
        p += 1
    return p


def check_for_deaths(players, locations, despair, hero_discard):
    # 1 Discard all cards from your hand.
    # 2 Advance the despair marker twice.
    # 3 Place your hero on their starting space and reset their health slider to full.
    for p in range(len(players)):
        if players[p].health <= 0:
            print(str(players[p].hero) + " has died!")
            despair += 2
            print("Despair has advanced by two!")
            hero_discard.extend(players[p].hand)
            players[p].hand = []
            for l in range(len(locations)):
                if (
                    locations[l].name == players[p].starting_space
                    and players[p].symbol not in locations[l].contents
                ):
                    locations[l].contents.append(players[p].symbol)
                elif (
                    locations[l].name != players[p].starting_space
                    and players[p].symbol in locations[l].contents
                ):
                    locations[l].contents.remove(players[p].symbol)
    return players, locations, despair, hero_discard
