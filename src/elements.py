import random
from abc import ABC, abstractmethod
from enum import Enum
from typing import Self

Coords = tuple[int, int]
Move = tuple[Coords]


class Printable(ABC):
    """
    класс реализации
    Элемент, выводимый на экран
    """

    @abstractmethod
    def render(self) -> None:
        pass


class PieceEnum(Enum):
    EMPTY = 0
    A = 1
    B = 2
    C = 3
    D = 4
    E = 5


class Piece(ABC):
    """
    класс анализа
    Элемент доски
    """

    _value: PieceEnum = PieceEnum.EMPTY

    @abstractmethod
    def set_value(self, val: PieceEnum) -> None:
        """
        post: set random value
        """

    @abstractmethod
    def set_random_value(self) -> None:
        """
        post: set random value
        """

    @abstractmethod
    def set_empty_value(self) -> None:
        """
        post: set empty value
        """

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, Piece):
            return value._value == self._value
        return False


class ConcretePiece(Piece):

    def __init__(self) -> None:
        super().__init__()
        self.set_empty_value()

    def set_random_value(self) -> None:
        self._value = random.choice(list(PieceEnum)[:1])

    def set_empty_value(self) -> None:
        self._value = PieceEnum.EMPTY

    def set_value(self, val: PieceEnum) -> None:
        self._value = val


class Points:
    """
    класс реализации
    значение счёта (обертка над int)
    """

    def __init__(self, points: int) -> None:
        self._points = points

    @property
    def value(self) -> int:
        return self._points

    def __add__(self, score: Self):
        return Points(self.value + score.value)

    def __sub__(self, score: Self):
        return Points(max(self.value - score.value, 0))


class Score(Printable):
    """
    класс анализа
    значение счёта игрока
    """

    _score: Points

    @abstractmethod
    def render(self) -> None:
        pass

    @abstractmethod
    def add_points(self, points: int) -> None:
        """
        post: self._points += points
        """

    @abstractmethod
    def remove_points(self, points: int) -> None:
        """
        cannot fail: if points <= self._points then self._points = 0
        post: self._points -= points
        """


class Board(Printable):
    """
    класс анализа
    игровая доска
    """

    _matrix: list[list[Piece]]
    _move_status = -1

    @abstractmethod
    def move(self) -> None:
        """
        pre : move is valid
        post: pieces swaped
        post: board processed
        """

    @abstractmethod
    def _delete_elements(self) -> None:
        """
        post: элементы, давшие комбинации, становятся пустыми
        post: обновлен лог какие элементы были "уничтожены"
        """

    @abstractmethod
    def _shift_elements(self) -> None:
        """
        post: не-пустые элементы смещены вниз на место пустых
        """

    @abstractmethod
    def _add_new_elements(self) -> None:
        """
        post: пустые элементы заменены на новые (случайные)
        """

    @abstractmethod
    def render(self) -> None:
        pass

    # query
    def get_move_status(self) -> int:
        return self._move_status


class ConcreteBoard8X8(Board):
    def __init__(self) -> None:
        super().__init__()
        self._matrix = [[ConcretePiece()] * 8] * 8


class Bonus(ABC):
    """
    класс анализа
    бонус, влияющий на игру. применяемый игроком
    """

    _board: Board

    @abstractmethod
    def apply_bonus(self) -> None:
        """
        post: board state changed
        """


class BonusList(Printable):
    """
    класс анализа
    список бонусов, доступных игроку
    """

    _bonus_list: set[Bonus]
    _remove_bonus_status: int = -1

    # commands
    @abstractmethod
    def add_bouns(self, bonus: Bonus) -> None:
        """
        post: bonus added to set
        """

    @abstractmethod
    def remove_bouns(self, bonus: Bonus) -> None:
        """
        pre : has bonus
        post: bonus removed from set
        """

    # query
    @abstractmethod
    def has_bouns(self, bonus: Bonus) -> bool:
        pass

    def get_remove_bonus_status(self) -> int:
        return self._remove_bonus_status


class MatchHandler(ABC):
    """
    класс реализации
    механика поиска комбинаций на поле
    """

    _board: Board
    _score: Score
    _process_matches_status = -1

    # command
    @abstractmethod
    def process_matches(self) -> None:
        """
        pre : has matches
        post: matched pieces are empty
        post: score increased
        """

    # query
    @abstractmethod
    def has_matches(self) -> bool:
        pass

    def process_matches_status(self) -> int:
        return self._process_matches_status


class Combinations(ABC):
    """
    класс реализации
    получение значений счёта и бонусов из уничтоженных элементов
    """

    _picies: dict[Piece, int]

    # queries
    @abstractmethod
    def get_value(self) -> Points:
        pass

    @abstractmethod
    def get_bonus(self) -> Bonus:
        pass
