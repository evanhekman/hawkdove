import simulation


def main():
    pops1 = simulation.simulate(0.25, 0.50, 0.25, 0, 5000)
    last_pop = pops1[-1]
    # continue with a tiny addition of retaliator
    pops2 = simulation.simulate(
        last_pop[0] - 0.01, last_pop[1] - 0.01, last_pop[2], 0.02, 5000
    )
    simulation.matplotlib_bs(
        0.25, 0.50, 0.25, 0, pops1 + pops2, "Perturbation halfway through"
    )


if __name__ == "__main__":
    main()
