# python imports
import math
import random

# external imports
import click

# local imports
import core
import matplotlib.pyplot as plt
import numpy as np

# constant value introduced into replicator equation to mimic continuity
LEARNING_RATE = 0.01


def simulate(
    h_pop: float,
    d_pop: float,
    b_pop: float,
    r_pop: float,
    iterations: int,
    noise: float = 0,
    bounds: bool = True,
) -> list[list[float]]:
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
        avg_fitness = np.mean(fitness)
        change = (fitness - avg_fitness) / avg_fitness

        if noise != 0:
            population = np.array(
                [x + (random.random() - 0.5) * noise for x in population]
            )

        # apply change based on who is doing well
        population = population * (1 + LEARNING_RATE * change)
        population = population / sum(population)
        # make sure we don't drift away from floating point errors
        assert math.isclose(sum(population), 1, abs_tol=0.001)

        if bounds:
            population = np.clip(population, 0, 1)
            # no negative populations
            assert all(p >= 0 for p in population)

        populations.append(population)

    return populations


def matplotlib_bs(
    hawk: float, dove: float, bully: float, retaliator: float, pops, title
):
    """
    All the matplotlib boilerplate...
    Themes from presentation: #092f53, #e2e2e2
    """
    pops_array = np.array(pops)
    hawks = pops_array[:, 0]
    doves = pops_array[:, 1]
    bullies = pops_array[:, 2]
    retaliators = pops_array[:, 3]
    time_steps = range(len(pops))

    plt.figure(figsize=(12, 8), facecolor="#e2e2e2")
    plt.plot(time_steps, hawks, label="Hawk", linewidth=2)
    plt.plot(time_steps, doves, label="Dove", linewidth=2)
    plt.plot(time_steps, bullies, label="Bully", linewidth=2)
    plt.plot(time_steps, retaliators, label="Retaliator", linewidth=2)

    ax = plt.gca()
    ax.set_facecolor("#e2e2e2")
    for spine in ax.spines.values():
        spine.set_color("#092f53")
        spine.set_linewidth(1.5)
    ax.spines["top"].set_visible(True)
    ax.spines["right"].set_visible(True)
    plt.xlabel("Iteration", color="#092f53", fontsize=20)
    plt.ylabel("Population(s)", color="#092f53", fontsize=20)
    plt.title(title, color="#092f53", fontsize=32)
    ax.tick_params(labelsize=16)
    ax.legend(
        bbox_to_anchor=(1.05, 1),
        loc="upper left",
        labelcolor="#092f53",
        fontsize=12,
        frameon=True,
        edgecolor="#092f53",
        facecolor="#e2e2e2",
        fancybox=False,
    )
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
@click.option("--title", "-t", type=str, default="")
@click.option("--noise", type=float, default=0)
@click.option("--bounds", type=bool, default=True)
@click.option("--graph", "-g", type=bool, default=True)
def main(hawk, dove, bully, retaliator, iterations, noise, title, bounds, graph):
    if sum([hawk, dove, bully, retaliator]) != 1:
        s = sum([hawk, dove, bully, retaliator])
        hawk /= s
        dove /= s
        bully /= s
        retaliator /= s
        print(
            "Automatically normalized starting populations:",
            hawk,
            dove,
            bully,
            retaliator,
        )

    pops = simulate(hawk, dove, bully, retaliator, iterations, noise, bounds)
    print("final values: ", pops[-1])
    if graph:
        matplotlib_bs(hawk, dove, bully, retaliator, pops, title)


if __name__ == "__main__":
    main()
