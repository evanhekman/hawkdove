# python imports
import math
import random

# external imports
import click
import matplotlib.pyplot as plt
import numpy as np

# local imports
import hawkdove


def simulate(h_pop, d_pop, b_pop, r_pop, iterations):
    """
    Runs a simulation based on the given starting populations.
    """
    population = np.array([h_pop, d_pop, b_pop, r_pop])
    if not math.isclose(sum(population), 1):
        print("Starting population should sum to 1.0")
        exit(1)

    # populations = [population]
    populations = []

    for i in range(iterations):
        # as described here:
        # https://en.wikipedia.org/wiki/Replicator_equation#:~:text=%5B4%5D-,Discrete,-replicator%20equation%5B
        fitness = np.array(
            [
                hawkdove.interaction(hawkdove.HAWK, population),
                hawkdove.interaction(hawkdove.DOVE, population),
                hawkdove.interaction(hawkdove.BULL, population),
                hawkdove.interaction(hawkdove.RETA, population),
            ]
        )
        avg_fitness = sum(fitness) / len(fitness)
        change = (fitness - avg_fitness) / avg_fitness
        population = np.array([x + random.random() * 0.01 for x in population])
        population = np.clip(population + 0.01 * change, 0.01, 0.97)
        population = population / sum(population)
        populations.append(population)

        # make sure we don't drift away from floating point errors
        assert math.isclose(sum(population), 1, abs_tol=0.01)
        # no negative populations
        assert all(p >= 0 for p in population)

    return populations


def matplotlib_bs(
    hawk: float, dove: float, bully: float, retaliator: float, pops: list[np.ndarray]
):
    """
    All the matplotlib boilerplate...
    """
    pops_array = np.array(pops)
    hawks = pops_array[:, 0]
    doves = pops_array[:, 1]
    bullies = pops_array[:, 2]
    retaliators = pops_array[:, 3]
    time_steps = range(len(pops))

    plt.figure(figsize=(10, 6))
    plt.plot(time_steps, hawks, label="Hawk", linewidth=2)
    plt.plot(time_steps, doves, label="Dove", linewidth=2)
    plt.plot(time_steps, bullies, label="Bully", linewidth=2)
    plt.plot(time_steps, retaliators, label="Retaliator", linewidth=2)

    plt.xlabel("Iteration")
    plt.ylabel("Population(s)")
    plt.title(f"Hawk-Dove-Bully-Retaliator ({hawk}, {dove}, {bully}, {retaliator})")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


@click.command
@click.option("--hawk", "--hawk-pop", "--h-pop", "-h", type=float, required=True)
@click.option("--dove", "--dove-pop", "--d-pop", "-d", type=float, required=True)
@click.option("--bully", "--bully-pop", "--b-pop", "-b", type=float, required=True)
@click.option(
    "--retaliator", "--retaliator-pop", "--r-pop", "-r", type=float, required=True
)
@click.option("--iterations", "-i", type=int, required=True)
@click.option("--graph", "-g", type=bool, default=True)
def main(hawk, dove, bully, retaliator, iterations, graph):
    pops = simulate(hawk, dove, bully, retaliator, iterations)
    # print("final values: ", pops[-1])
    if graph:
        matplotlib_bs(hawk, dove, bully, retaliator, pops)


if __name__ == "__main__":
    main()
