# python imports
import math

# external imports
import click
import matplotlib.pyplot as plt
import numpy as np

# local imports
import hawkdove as hawkdove


def simulate(h_pop, d_pop, b_pop, r_pop, iterations):
    population = np.array([h_pop, d_pop, b_pop, r_pop])
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


@click.command
@click.argument("p_hawk", type=float)
@click.argument("p_dove", type=float)
@click.argument("p_bully", type=float)
@click.argument("p_retaliator", type=float)
@click.argument("iterations", type=int)
@click.argument("graph", type=bool, default=True)
def main(p_hawk, p_dove, p_bully, p_retaliator, iterations, graph):
    pops = simulate(p_hawk, p_dove, p_bully, p_retaliator, iterations)
    if graph:
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
        plt.title(
            f"Hawk-Dove-Bully-Retaliator ({p_hawk}, {p_dove}, {p_bully}, {p_retaliator})"
        )
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    main()
