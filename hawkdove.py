import enum

import numpy as np


class Strategy(enum.Enum):
    HAWK = (1, 0, 0, 0)
    DOVE = (0, 1, 0, 0)
    BULLY = (0, 0, 1, 0)
    RETALIATOR = (0, 0, 0, 1)


PAYOFF = np.array(
    [
        [-25, 50, 50, -25],
        [0, 15, 0, 15],
        [0, 50, 25, 0],
        [-25, 15, 50, 15],
    ]
)


def interaction(p1: np.ndarray, p2: np.ndarray):
    return float(p1 @ PAYOFF @ p2), float(p2 @ PAYOFF @ p1)


def main():
    try:
        i = 0
        player1 = 0
        player2 = 0
        while True:
            print("HAWK - 0, DOVE - 1, BULLY - 2, RETALIATOR - 3")
            print("player 1 select strategy: ")
            index1 = int(input())
            arr1 = [0] * 4
            arr1[index1] = 1
            strat1 = np.array(arr1)
            print("player 2 select strategy: ")
            index2 = int(input())
            arr2 = [0] * 4
            arr2[index2] = 1
            strat2 = np.array(arr2)
            r1, r2 = interaction(strat1, strat2)
            player1 += r1
            player2 += r2
            print(f"Round {i}: Player 1 has {player1}, Player 2 has {player2}")
            i += 1
    except KeyboardInterrupt:
        print("terminating")


if __name__ == "__main__":
    main()
