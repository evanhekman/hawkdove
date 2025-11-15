import random

import numpy as np

import hawkdove

letters = ["H", "D", "B", "R"]


def classify_distribution(strats: list):
    """
    Based on a list, orders [H]awks [D]oves [B]ullies and [R]etaliators into a string.
    """
    indices = enumerate(strats)
    sorts = reversed(sorted(indices, key=lambda x: x[1]))
    s = ""
    for x in sorts:
        s += letters[x[0]]
    return s


def generate_distribution(ordering: str):
    """
    Takes a string (like the ones form classify_distribution) and converts to bespoke distribution
    """
    dist = [0.0] * 4
    dist[letters.index(ordering[0])] = 0.4
    dist[letters.index(ordering[1])] = 0.3
    dist[letters.index(ordering[2])] = 0.2
    dist[letters.index(ordering[3])] = 0.1
    return dist


def random_100() -> list[float]:
    # Generate 3 random cut points in [0, 100]
    cuts = sorted([random.randint(0, 100) for _ in range(3)])
    return [cuts[0], cuts[1] - cuts[0], cuts[2] - cuts[1], 100 - cuts[2]]


def main():
    winners = {
        "H": 0,
        "D": 0,
        "B": 0,
        "R": 0,
    }
    # for 1000 random distributions
    iterations = 100000
    for i in range(iterations):
        dist = random_100()
        random.shuffle(dist)
        assert sum(dist) == 100
        population = np.array([d / 100.0 for d in dist])
        results = [
            hawkdove.interaction(hawkdove.HAWK, population),
            hawkdove.interaction(hawkdove.DOVE, population),
            hawkdove.interaction(hawkdove.BULL, population),
            hawkdove.interaction(hawkdove.RETA, population),
        ]
        assert results[0] != results[1]
        winner = classify_distribution(results)[0]
        winners[winner] += 1
    print(winners)
    print("hawk wins ", round(winners["H"] / iterations * 100, 2), " % of encounters")
    print("dove wins ", round(winners["D"] / iterations * 100, 2), " % of encounters")
    print("bully wins ", round(winners["B"] / iterations * 100, 2), " % of encounters")
    print(
        "retaliator wins ",
        round(winners["R"] / iterations * 100, 2),
        " % of encounters",
    )


main()
