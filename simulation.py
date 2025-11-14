# python imports
import math

# external imports
import click
import matplotlib.pyplot as plt
import numpy as np

# local imports
import hawkdove as hawkdove


def simulate(h_pop, d_pop, b_pop, r_pop, iterations):
    """
    Runs a simulation based on the given starting populations.
    """
    population = np.array([h_pop, d_pop, b_pop, r_pop])
    if not math.isclose(sum(population), 1):
        print("Starting population should sum to 1.0")
        exit(1)

    populations = [population]
    h_strat = np.array([1, 0, 0, 0])
    d_strat = np.array([0, 1, 0, 0])
    b_strat = np.array([0, 0, 1, 0])
    r_strat = np.array([0, 0, 0, 1])

    for i in range(iterations):
        scores = np.array(
            [
                h_pop * hawkdove.interaction(h_strat, population),
                d_pop * hawkdove.interaction(d_strat, population),
                b_pop * hawkdove.interaction(b_strat, population),
                r_pop * hawkdove.interaction(r_strat, population),
            ]
        )
        population = scores / sum(scores)
        populations.append(population)

        # make sure we don't drift away from floating point errors
        assert math.isclose(sum(population), 1)

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
    print("final values: ", pops[-1])
    if graph:
        matplotlib_bs(hawk, dove, bully, retaliator, pops)


if __name__ == "__main__":
    main()
