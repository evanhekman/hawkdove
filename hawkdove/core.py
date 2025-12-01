import numpy as np

HAWK = np.array([1, 0, 0, 0])
DOVE = np.array([0, 1, 0, 0])
BULL = np.array([0, 0, 1, 0])
RETA = np.array([0, 0, 0, 1])

PAYOFF = np.array(
    [
        [-25, 50, 50, -25],  # hawk
        [0, 15, 0, 15],  # dove
        [0, 50, 25, 0],  # bully
        [-25, 15, 50, 15],  # retaliator
    ]
)

# modified matrix with nonnegative entries to simplify simulation logic
MODIFIED_PAYOFF = PAYOFF + 50


def interaction(p1: np.ndarray, p2: np.ndarray):
    # return float(p1 @ PAYOFF @ p2)
    return float(p1 @ MODIFIED_PAYOFF @ p2)


def main():
    try:
        i = 0
        player1 = 0
        player2 = 0
        while True:
            print("HAWK - 0, DOVE - 1, BULLY - 2, RETALIATOR - 3")

            # player 1
            print("player 1 select strategy: ")
            arr1 = [0] * 4
            arr1[int(input())] = 1
            strat1 = np.array(arr1)

            # player 2
            print("player 2 select strategy: ")
            arr2 = [0] * 4
            arr2[int(input())] = 1
            strat2 = np.array(arr2)

            # rewards
            reward1, reward2 = interaction(strat1, strat2), interaction(strat2, strat1)
            player1 += reward1
            player2 += reward2
            print(
                f"Round {i}: Player 1 has {player1 - reward1} -> {player1}, Player 2 has {player2 - reward2} -> {player2}"
            )
            i += 1

    except KeyboardInterrupt:
        print("terminating")


if __name__ == "__main__":
    main()
