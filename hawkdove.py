import enum


class Strategy(enum.Enum):
    HAWK = 0
    DOVE = 1
    BULLY = 2
    RETALIATOR = 3


def interaction(strat1, strat2) -> tuple[int, int]:
    match strat1:
        case Strategy.HAWK:
            match strat2:
                case Strategy.HAWK:
                    return -25, -25
                case Strategy.DOVE:
                    return 50, 0
                case Strategy.BULLY:
                    return 50, 0
                case Strategy.RETALIATOR:
                    return -25, -25
                case _:
                    raise ValueError("Invalid strategy")
        case Strategy.DOVE:
            match strat2:
                case Strategy.HAWK:
                    return 0, 50
                case Strategy.DOVE:
                    return 15, 15
                case Strategy.BULLY:
                    return 0, 50
                case Strategy.RETALIATOR:
                    return 15, 15
                case _:
                    raise ValueError("Invalid strategy")
        case Strategy.BULLY:
            match strat2:
                case Strategy.HAWK:
                    return 0, 50
                case Strategy.DOVE:
                    return 50, 0
                case Strategy.BULLY:
                    return 25, 25
                case Strategy.RETALIATOR:
                    return 0, 50
                case _:
                    ...
        case Strategy.RETALIATOR:
            match strat2:
                case Strategy.HAWK:
                    return -25, -25
                case Strategy.DOVE:
                    return 15, 15
                case Strategy.BULLY:
                    return 50, 0
                case Strategy.RETALIATOR:
                    return 15, 15
                case _:
                    ...
        case _:
            raise ValueError("Invalid strategy")
    # to avoid type checker errors
    return 0, 0


def main():
    try:
        i = 0
        player1 = 0
        player2 = 0
        while True:
            print("HAWK - 0, DOVE - 1, BULLY - 2, RETALIATOR - 3")
            print("player 1 select strategy: ")
            strat1 = Strategy(int(input()))
            print("player 2 select strategy: ")
            strat2 = Strategy(int(input()))
            r1, r2 = interaction(strat1, strat2)
            player1 += r1
            player2 += r2
            print(f"Round {i}: Player 1 has {player1}, Player 2 has {player2}")
            i += 1
    except KeyboardInterrupt:
        print("terminating")


if __name__ == "__main__":
    main()
