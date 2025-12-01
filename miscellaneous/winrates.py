"""
This file contains code to estimate how often each strategy wins across random distributions.

- Random distributions are generated through randomized cuts of
"""

import random
import sys

import numpy as np

import hawkdove.core as hawkdove

letters = ["H", "D", "B", "R", "P"]


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


def random_100() -> list[int]:
    cuts = sorted([random.randint(0, 100) for _ in range(3)])
    numbers = [cuts[0], cuts[1] - cuts[0], cuts[2] - cuts[1], 100 - cuts[2]]
    random.shuffle(numbers)
    assert sum(numbers) == 100
    return numbers


def calculate_fraction_winners():
    winners = {
        "H": 0,
        "D": 0,
        "B": 0,
        "R": 0,
    }
    iterations = 1000000
    print(f"testing {iterations} random populations...")
    for i in range(iterations):
        if i % (iterations // 100) == 0:
            if i % (iterations // 10) == 0:
                sys.stdout.write(f"{int(i / (iterations // 100))}%")
            else:
                sys.stdout.write(".")
            sys.stdout.flush()
        dist = random_100()
        population = np.array([d / 100.0 for d in dist])
        results = [
            hawkdove.interaction(hawkdove.HAWK, population),
            hawkdove.interaction(hawkdove.DOVE, population),
            hawkdove.interaction(hawkdove.BULL, population),
            hawkdove.interaction(hawkdove.RETA, population),
        ]
        assert results[0] != results[1]  # this code isn't designed to handle ties
        winner = classify_distribution(results)[0]
        winners[winner] += 1
    sys.stdout.write("100%")
    sys.stdout.flush()
    print()
    print("hawk wins ", round(winners["H"] / iterations * 100, 2), " % of encounters")
    print("dove wins ", round(winners["D"] / iterations * 100, 2), " % of encounters")
    print("bully wins ", round(winners["B"] / iterations * 100, 2), " % of encounters")
    print(
        "retaliator wins ",
        round(winners["R"] / iterations * 100, 2),
        " % of encounters",
    )


if __name__ == "__main__":
    calculate_fraction_winners()
