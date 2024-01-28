from random import sample


def roll(num_dice):
    assert num_dice > 0
    res = {"attack": 0, "defend": 0}
    die = ["1A", "1A", "2A", "1D", "1A", "1A1D"]
    s = sample(die, num_dice)
    for r in s:
        if r == "1A":
            res["attack"] += 1
        elif r == "1D":
            res["defend"] += 1
        elif r == "2A":
            res["attack"] += 2
        elif r == "1A1D":
            res["defend"] += 1
            res["attack"] += 1

    return res
