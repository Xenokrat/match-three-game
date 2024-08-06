from abc import ABC, abstractmethod

from .elements import *

State = tuple[Board, Score, BonusList]


class History(ABC):
    """
    класс проектирования
    последовательность состояний игры
    """

    _state_list: list[State]

    @abstractmethod
    def add_state(self, state: State) -> None:
        """
        post: added new state to list
        """

    @abstractmethod
    def undo(self) -> None:
        """
        post: remove last state from list
        """


class Game(ABC):
    """
    класс анализа
    игра и управление ей
    """

    _game_elements: list[Printable]
    _history: History

    @abstractmethod
    def render_game(self) -> None:
        """
        post: game rendered in console
        """


class GameFactory(ABC):
    """
    класс проектирования
    создание новой игры
    """

    # query
    @abstractmethod
    def create_new_game(self) -> Game:
        """
        returns new game
        """


class Command(ABC):
    """
    класс реализации
    действия игрока, влияющие на игру
    """

    # command
    @abstractmethod
    def execute(self) -> None:
        """
        post: game updated or ended
        """


class MoveCommand(Command):

    def __init__(self, board: Board) -> None:
        super().__init__()
        self._board = board


class BonusCommand(Command):

    def __init__(self, bonus_list: BonusList) -> None:
        super().__init__()
        self._bonus_list = bonus_list


class GameCommand(Command):

    def __init__(self, game: Game) -> None:
        super().__init__()
        self._game = game
