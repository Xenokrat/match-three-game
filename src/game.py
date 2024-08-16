import os
import sys
from abc import ABC, abstractmethod
from time import sleep

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


class ConcreteHistory(History):

    def __init__(self) -> None:
        self._state_list: list[State] = []

    def add_state(self, state: State) -> None:
        """
        post: added new state to list
        """

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

    @abstractmethod
    def add_element(self, element: Printable) -> None:
        """
        post: game rendered in console
        """

    # query
    @abstractmethod
    def get_game_board(self) -> Board:
        pass

    @abstractmethod
    def get_game_score(self) -> Score:
        pass


class ConcreteGame(Game):
    def __init__(self) -> None:
        self._game_elements: list[Printable] = []
        self._history: History = ConcreteHistory()

    def add_element(self, element: Printable) -> None:
        self._game_elements.append(element)

    def render_game(self) -> None:
        for i in self._game_elements:
            i.render()

    def get_game_board(self) -> Board:
        for el in self._game_elements:
            if isinstance(el, Board):
                return el
        raise Exception("Game board not initialized for some reason")

    def get_game_score(self) -> Score:
        for el in self._game_elements:
            if isinstance(el, Score):
                return el
        raise Exception("Game board not initialized for some reason")


class GameFactory(ABC):
    """
    класс проектирования
    создание новой игры
    """

    # query
    @staticmethod
    @abstractmethod
    def create_new_game() -> Game:
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

    def __init__(self, board: Board, score: Score, command: str) -> None:
        super().__init__()
        self._board = board
        self._score = score
        self._command = command

    def execute(self) -> None:
        """
        post: game updated or ended
        """
        args = self._command.split(",")
        str_coord1, str_coord2 = args[0], args[1]
        if not (
            self._validate_coords(str_coord1) and self._validate_coords(str_coord2)
        ):
            InvalidCommand(self._command).execute()
            return
        coord1 = int(str_coord1[0]) - 1, int(str_coord1[1]) - 1
        coord2 = int(str_coord2[0]) - 1, int(str_coord2[1]) - 1
        self._board.move(coord1, coord2)
        comb_handler = CombHandler(self._board, self._score)
        comb_handler.process_combs()

        if self._board.get_move_status == 0:
            InvalidCommand(self._command, msg="Bad command input").execute()

    def _validate_coords(self, str_coord: str) -> bool:
        if len(str_coord) != 2:
            return False
        board_size = self._board.get_size()
        if int(str_coord[0]) - 1 < 0 or int(str_coord[0]) > board_size:
            return False
        if int(str_coord[1]) - 1 < 0 or int(str_coord[1]) > board_size:
            return False
        return True


class BonusCommand(Command):

    def __init__(self, bonus_list: BonusList) -> None:
        super().__init__()
        self._bonus_list = bonus_list


class GameCommand(Command):

    def __init__(self, game: Game) -> None:
        super().__init__()
        self._game = game


class EndGameCommand(Command):
    def execute(self) -> None:
        sys.exit(0)


class InvalidCommand(Command):
    def __init__(self, command: str, msg="") -> None:
        super().__init__()
        self._command = command
        self._msg = msg

    def execute(self) -> None:
        print(f'Command "{self._command}" is invalid, please try again')
        print(self._msg)
        sleep(1)


class ConcreteGameFactory(GameFactory):

    @staticmethod
    def create_new_game() -> ConcreteGame:
        game = ConcreteGame()
        board = ConcreteBoard8X8()
        score = ConcreteScore()
        bonus_list = ConcreteBonusList()
        game.add_element(board)
        game.add_element(score)
        game.add_element(bonus_list)
        algo = CombHandler(board, score)
        algo.prepare_board()
        return game


class AbsCommandDispatcher(ABC):

    @abstractmethod
    def process_command(self) -> Command | None:
        pass


class CommandDispatcher(AbsCommandDispatcher):
    def __init__(self, command: str, game: Game) -> None:
        self._command = command
        self._game = game

    def process_command(self) -> Command:
        if self._command == "q":
            return EndGameCommand()
        args = self._command.split(",")
        if len(args) == 2 and args[0].isdigit() and args[1].isdigit():
            board = self._game.get_game_board()
            score = self._game.get_game_score()
            return MoveCommand(board, score, self._command)
        return InvalidCommand(self._command)


class AbsGameLoop(ABC):

    def __init__(self, game: Game) -> None:
        self._game = game

    @abstractmethod
    def run_game_loop(self):
        pass


class GameLoop(AbsGameLoop, Printable):

    def run_game_loop(self):
        while True:
            self.clear_screen()
            self._game.render_game()
            command = self._get_player_input()
            cmd = CommandDispatcher(command, self._game).process_command()
            cmd.execute()

    def _get_player_input(self):
        command = (
            input(
                'Enter command ("[row][col],[row][col]" to swap elements (11,12 for example), q to quit): '
            )
            .strip()
            .lower()
        )
        return command
