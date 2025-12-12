"""
This file contains code to estimate how often each strategy wins across random distributions.

- Random distributions are generated through randomized cuts of
"""

import math
import random
import sys

import matplotlib.pyplot as plt
import numpy as np

import hawkdove.core as hawkdove

letters = ["H", "D", "B", "R"]


def get_winner(strats: list):
    """
    Based on a list, orders [H]awks [D]oves [B]ullies and [R]etaliators into a string.
    """
    indices = enumerate(strats)
    sorts = reversed(sorted(indices, key=lambda x: x[1]))
    s = ""
    for x in sorts:
        s += letters[x[0]]
    return s


# def get_survivors(strats: list):
#     s = []
#     for i in range(4):
#         if strats[i] > 0.01:
#             s.append(letters[i])
#     return s


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


def random_dist() -> list[float]:
    # cuts = sorted([random.randint(0, 100) for _ in range(3)])
    # numbers = [cuts[0], cuts[1] - cuts[0], cuts[2] - cuts[1], 100 - cuts[2]]
    numbers = [random.random() for _ in range(4)]
    s = sum(numbers)
    numbers = [numbers[i] / s for i in range(4)]
    random.shuffle(numbers)
    assert math.isclose(sum(numbers), 1.0)
    return numbers


def calculate_fraction_winners():
    winners = {
        "H": 0,
        "D": 0,
        "B": 0,
        "R": 0,
    }
    survivors = {
        "H": 0,
        "D": 0,
        "B": 0,
        "R": 0,
    }
    iterations = 1000
    dists = []
    print(f"testing {iterations} random populations...")
    for i in range(iterations):
        if i % (iterations // 100) == 0:
            if i % (iterations // 10) == 0:
                sys.stdout.write(f"{int(i / (iterations // 100))}%")
            else:
                sys.stdout.write(".")
            sys.stdout.flush()
        dist = random_dist()
        dists.append(dist)
        benefit = random.randint(1, 10)
        cost = random.randint(1, 10)
        payoff = hawkdove.generate_matrix(benefit, cost)
        og_pop = np.array(dist)
        pop = og_pop
        last_pop = np.array([0, 0, 0, 0])

        i = 0
        while not math.isclose(
            sum(abs(pop[i] - last_pop[i]) for i in range(4)), 0, abs_tol=0.000000001
        ):
            last_pop = pop
            i += 1
            # as described here:
            # https://en.wikipedia.org/wiki/Replicator_equation#:~:text=%5B4%5D-,Discrete,-replicator%20equation%5B
            fitness = np.array(
                [
                    hawkdove.interaction(hawkdove.HAWK, pop, payoff),
                    hawkdove.interaction(hawkdove.DOVE, pop, payoff),
                    hawkdove.interaction(hawkdove.BULL, pop, payoff),
                    hawkdove.interaction(hawkdove.RETA, pop, payoff),
                ]
            )
            avg_fitness = np.mean(fitness)
            change = fitness - avg_fitness

            # apply change based on who is doing well
            pop = pop * (1 + 0.1 * change)
            pop = pop / sum(pop)
            # make sure we don't drift away from floating point errors
            assert math.isclose(sum(pop), 1, abs_tol=0.001)
            assert all(p >= 0 for p in pop)

        if i % 100 == 0:
            print()
            print(og_pop, i, pop, cost, benefit)
            print()
        winner = get_winner(list(pop))[0]
        for p in range(len(pop)):
            if pop[p] > 0.01:
                survivors[letters[p]] += 1
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
    print()
    print(
        "hawk survives ",
        round(survivors["H"] / iterations * 100, 2),
        " % of encounters",
    )
    print(
        "dove survives ",
        round(survivors["D"] / iterations * 100, 2),
        " % of encounters",
    )
    print(
        "bully survives ",
        round(survivors["B"] / iterations * 100, 2),
        " % of encounters",
    )
    print(
        "retaliator survives ",
        round(survivors["R"] / iterations * 100, 2),
        " % of encounters",
    )
    print()

    # graph dists
    dists_flat = [val for dist in dists for val in dist]
    plt.hist(dists_flat, bins=100)
    plt.show()


if __name__ == "__main__":
    calculate_fraction_winners()
