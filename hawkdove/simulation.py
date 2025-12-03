# python imports
import math
import random

# external imports
import click

# local imports
import core
import matplotlib.pyplot as plt
import numpy as np


def simulate(
    h_pop: float,
    d_pop: float,
    b_pop: float,
    r_pop: float,
    iterations: int,
    noise: float = 0,
    bounds: bool = True,
):
    """
    Runs a simulation based on the given starting populations.
        h_pop: starting hawk population
        d_pop: starting dove population
        b_pop: starting bully population
        r_pop: starting retaliator population
        iterations: how many iterations to run
        noise: maximum change resulting from noise
        bounds: whether to clamp populations in the [0, 1] range
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
                core.interaction(core.HAWK, population),
                core.interaction(core.DOVE, population),
                core.interaction(core.BULL, population),
                core.interaction(core.RETA, population),
            ]
        )
        avg_fitness = sum(fitness) / len(fitness)
        change = (fitness - avg_fitness) / avg_fitness

        if noise != 0:
            population = np.array(
                [x + (random.random() - 0.5) * noise for x in population]
            )

        # apply change based on who is doing well
        population = population * (1 + 0.01 * change)
        population = population / sum(population)
        # make sure we don't drift away from floating point errors
        assert math.isclose(sum(population), 1, abs_tol=0.01)

        if bounds:
            population = np.clip(population, 0, 1)
            # no negative populations
            assert all(p >= 0 for p in population)

        populations.append(population)

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
@click.option("--noise", type=float, default=0)
@click.option("--bounds", type=bool, default=True)
@click.option("--graph", "-g", type=bool, default=True)
def main(hawk, dove, bully, retaliator, iterations, noise, bounds, graph):
    pops = simulate(hawk, dove, bully, retaliator, iterations, noise, bounds)
    print("final values: ", pops[-1])
    if graph:
        matplotlib_bs(hawk, dove, bully, retaliator, pops)


if __name__ == "__main__":
    main()
