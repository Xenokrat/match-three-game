from abc import ABC

from .utils import _CommandStatus


class GameElements(ABC):

    # constructor
    def __init__(self, matrix: Matrix, history: History) -> None:
        self._matrix = matrix
        self._history = history

        self._accept_command_status = _CommandStatus.NIL

    # commands
    def create_matrix(self) -> None:
        """
        pre:
        post: матрица (пере)создана
        """

    def clear_history(self) -> None:
        """
        pre:
        post: история очищена
        """

    def undo_history(self) -> None:
        """
        pre:  история не пустая
        post: история -1
        """

    def accept_command(self, command: UserCommand) -> None:
        """
        pre:  команда валидна
        post: элементы игры изменены соответственно команде, или игра закончена
        """

    # queries
    def get_accept_command_status(self) -> _CommandStatus:
        return self._accept_command_status


class Game(ABC):

    # constructor
    def __init__(self, ui: AdtUserInterface, game_elements: GameElements) -> None:
        self._ui = ui
        self._game_elements = game_elements

        self._accept_command_status = _CommandStatus.NIL

    # commands
    def draw_ui(self) -> None:
        """
        pre:
        post: ui выведен на экран
        """

    def start_game(self) -> None:
        """
        pre:
        post: инициализированы элементы игры: поле, счёт, бонусы
        """

    def end_game(self) -> None:
        """
        pre:
        post: игра закончена
        """

    def restart_game(self) -> None:
        """
        pre:
        post: игра пересоздана
        """

    def accept_command(self, command: UserCommand) -> None:
        """
        pre:  команда валидна
        post: элементы игры изменены соответственно команде, или игра закончена
        post: ui перерисован
        """

    # queries
    def get_accept_command_status(self) -> _CommandStatus:
        return self._accept_command_status
