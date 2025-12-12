import simulation


def main():
    # NOTE: just manually edited this one, no cli tooling
    pops1 = simulation.simulate(1, 0, 0, 0, 500)
    last_pop = pops1[-1]
    # continue with a tiny addition of retaliator
    pops2 = simulation.simulate(
        last_pop[0] - 0.01, last_pop[1], last_pop[2], last_pop[3] + 0.01, 3000
    )
    simulation.matplotlib_bs(pops1 + pops2, "Hawk-Bully disturbed by Retaliators")


if __name__ == "__main__":
    main()
