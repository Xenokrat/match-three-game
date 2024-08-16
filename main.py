from src.elements import *
from src.game import *


def main() -> None:
    game = ConcreteGameFactory.create_new_game()
    game_loop = GameLoop(game)
    game_loop.run_game_loop()


if __name__ == "__main__":
    main()
