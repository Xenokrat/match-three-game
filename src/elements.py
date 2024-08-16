import os
import random
from abc import ABC, abstractmethod
from enum import Enum
from shutil import get_terminal_size
from time import sleep
from typing import Protocol, Self

Coords = tuple[int, int]
Move = tuple[Coords]


class Printable(Protocol):
    """
    класс реализации
    Элемент, выводимый на экран
    """

    def render(self) -> None:
        pass

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def vertical_center_print(self, obj_size: int = 8, end="\n") -> None:
        _, rows = get_terminal_size()
        rows = int(rows * 0.4)
        grid_height = obj_size
        top_padding = max((rows - grid_height) // 2, 0)
        for _ in range(top_padding):
            print()

    def horizontal_center_print(self, printable, obj_size: int = 8, end="\n") -> None:
        cols, _ = get_terminal_size()
        cols = int(cols * 0.4)
        grid_width = obj_size * 2  # each cell takes 2 spaces (e.g., 'P ')
        left_padding = max((cols - grid_width) // 2, 0)
        print(" " * left_padding + printable, end=end)


class PieceEnum(Enum):
    X = 0
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

    _value: PieceEnum = PieceEnum.X

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
    colors = {
        0: "\033[95m",
        1: "\033[94m",
        2: "\033[96m",
        3: "\033[92m",
        4: "\033[93m",
        5: "\033[91m",
    }

    def __init__(self) -> None:
        super().__init__()
        self.set_random_value()

    def set_random_value(self) -> None:
        self._value = random.choice(list(PieceEnum)[1:])

    def set_empty_value(self) -> None:
        self._value = PieceEnum.X

    def set_value(self, val: PieceEnum) -> None:
        self._value = val

    def __str__(self) -> str:
        return str(self.colors[self._value.value] + self._value.name + "\033[0m")


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

    def __str__(self) -> str:
        return str(self._points)


class AbsCombination(ABC):
    """
    класс реализации
    получение значений счёта и бонусов из уничтоженных элементов
    """

    _picies: dict[Piece, int]

    # queries
    @abstractmethod
    def get_score_points(self) -> Points:
        pass

    @abstractmethod
    def get_coords(self) -> set[Coords]:
        pass

    # @abstractmethod
    # def get_bonus(self) -> Bonus:
    #     pass


class Combination(AbsCombination):
    """
    класс реализации
    получение значений счёта и бонусов из уничтоженных элементов
    """

    def __init__(self, coords: set[Coords]) -> None:
        super().__init__()
        self._coords = coords

    def __hash__(self) -> int:
        return hash(self._coords)

    def get_coords(self) -> set[Coords]:
        return self._coords

    # queries
    def get_score_points(self) -> Points:
        length = len(self._coords)
        if length == 3:
            return Points(3)
        if length == 4:
            return Points(5)
        if length == 5:
            return Points(9)
        return Points(15)

    # def get_bonus(self) -> Bonus:
    #     # TODO:
    #     pass


class Score(Printable):
    """
    класс анализа
    значение счёта игрока
    """

    @abstractmethod
    def render(self) -> None:
        pass

    @abstractmethod
    def add_points(self, points: Points) -> None:
        """
        post: self._points += points
        """

    @abstractmethod
    def remove_points(self, points: int) -> None:
        """
        cannot fail: if points <= self._points then self._points = 0
        post: self._points -= points
        """


class ConcreteScore(Score):

    def __init__(self) -> None:
        super().__init__()
        self._score = Points(0)

    def render(self) -> None:
        print(f"Current Score: {self._score}")

    def add_points(self, points: Points) -> None:
        self._score += points

    def remove_points(self, points: int) -> None:
        self._score -= Points(points)


class Board(Printable):
    """
    класс анализа
    игровая доска
    """

    _matrix: list[list[Piece]]
    _move_status = -1

    @abstractmethod
    def move(self, coord1: Coords, coord2: Coords) -> None:
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
    @abstractmethod
    def get_board_piece(self, coord: Coords) -> Piece:
        row, col = coord
        return self._matrix[row][col]

    def get_move_status(self) -> int:
        return self._move_status

    def get_size(self) -> int:
        return len(self._matrix)


class ConcreteBoard8X8(Board):
    def __init__(self) -> None:
        super().__init__()
        self._matrix = [[ConcretePiece() for _ in range(8)] for _ in range(8)]

    def render(self) -> None:
        size = len(self._matrix)
        print("\n")
        print("     game ", end="")
        for i in range(size):
            print(f" {i + 1} |", end="")
        print("\n    ", end="")
        print("=" * (size * 4 + 6))
        for i, row in enumerate(self._matrix):
            print(f"    | {i + 1} || ", end="")
            print(" | ".join(str(cell) for cell in row), end="")
            print(" |")
            print("    ", end="")
            print("-" * (len(row) * 4 + 6))
        print("")

    def move(self, coord1: Coords, coord2: Coords) -> None:
        self._swap(coord1, coord2)
        self._validate_move(coord1, coord2)

        if not self.get_move_status():
            self._swap(coord2, coord1)
            return

    def _swap(self, coord1: Coords, coord2: Coords) -> None:
        row1, col1 = coord1
        row2, col2 = coord2
        tmp = self._matrix[row1][col1]
        self._matrix[row1][col1] = self._matrix[row2][col2]
        self._matrix[row2][col2] = tmp

    def _validate_move(self, coord1: Coords, coord2: Coords) -> bool:
        row1, col1 = coord1
        row2, col2 = coord2
        if not abs(row1 - row2) + abs(col1 - col2) == 1:
            return False
        return True

    def _delete_elements(self) -> None:
        pass

    def _shift_elements(self) -> None:
        pass

    def _add_new_elements(self) -> None:
        pass

    def get_move_status(self) -> int:
        return self._move_status

    def get_board_piece(self, coord: Coords) -> Piece:
        row, col = coord
        return self._matrix[row][col]


class Bonus(ABC):
    """
    класс анализа
    бонус, влияющий на игру. применяемый игроком
    """

    @abstractmethod
    def apply_bonus(self, board: Board) -> None:
        pass


class RemoveBonus(Bonus):

    def __init__(self) -> None:
        super().__init__()
        self._name = "Remove Bonus"

    def apply_bonus(self, board: Board) -> None:
        pass

    def __str__(self) -> str:
        return self._name


class AbsCombHandler(ABC):
    """
    класс реализации
    механика поиска комбинаций на поле
    """

    def __init__(self, board: Board, score: Score) -> None:
        self._board = board
        self._score = score
        self._combs: list[Combination] = []

    # command
    @abstractmethod
    def process_combs(self) -> None:
        """
        post: matched pieces are empty
        post: score increased
        """

    # query
    @abstractmethod
    def has_matches(self) -> bool:
        pass


class CombHandler(AbsCombHandler):

    # command
    def process_combs(self) -> None:
        self._find_combs()
        while True:
            sleep(1)
            self._remove_elements()
            self._board.clear_screen()
            self._board.render()
            sleep(1)
            self._shift_elements()
            self._board.clear_screen()
            self._board.render()
            sleep(1)
            self._replace_elements()
            self._board.clear_screen()
            self._board.render()
            sleep(1)
            self._update_score()
            self._clear_combs()
            self._find_combs()
            if not self.has_matches():
                break

    def prepare_board(self) -> None:
        while True:
            self._find_combs()
            if not self.has_matches():
                break
            self._prepare_board_elements()
            self._clear_combs()

    def _prepare_board_elements(self) -> None:
        matrix = self._get_matrix()
        for comb in self._combs:
            for coord in comb.get_coords():
                row, col = coord
                matrix[row][col].set_random_value()

    def _update_score(self) -> None:
        for comb in self._combs:
            self._score.add_points(comb.get_score_points())

    def _remove_elements(self) -> None:
        matrix = self._get_matrix()
        for comb in self._combs:
            for coord in comb.get_coords():
                row, col = coord
                matrix[row][col].set_empty_value()

    def _shift_elements(self) -> None:
        matrix = self._get_matrix()
        rows = len(matrix)
        cols = len(matrix[0])

        for c in range(cols):
            column = [matrix[r][c] for r in range(rows)]
            column.sort(key=lambda x: 0 if x._value.value > 0 else 1, reverse=True)
            for r in range(rows):
                matrix[r][c] = column[r]

    def _replace_elements(self) -> None:
        matrix = self._get_matrix()
        rows = len(matrix)
        cols = len(matrix[0])

        for r in range(rows):
            for c in range(cols):
                if matrix[r][c]._value == PieceEnum.X:
                    matrix[r][c].set_random_value()

    def _clear_combs(self) -> None:
        self._combs = []

    def _find_combs(self) -> None:
        """
        post: matched pieces are empty
        post: score increased
        """
        rows = cols = self._board.get_size()
        matrix = self._get_matrix()

        # TODO: write it better
        for r in range(rows):
            count = 1
            for c in range(1, cols):
                if matrix[r][c] == matrix[r][c - 1]:
                    count += 1
                else:
                    if count >= 3:
                        self._combs.append(
                            Combination({(r, x) for x in range(c - count, c)})
                        )
                    count = 1

            # Check for sequence at the end of the row
            if count >= 3:
                self._combs.append(
                    Combination({(r, x) for x in range(cols - count, cols)})
                )

        # TODO: write it better
        for c in range(cols):
            count = 1
            for r in range(1, rows):
                if matrix[r][c] == matrix[r - 1][c]:
                    count += 1
                else:
                    if count >= 3:
                        self._combs.append(
                            Combination({(x, c) for x in range(r - count, r)})
                        )
                    count = 1

            # Check for sequence at the end of the column
            if count >= 3:
                self._combs.append(
                    Combination({(x, c) for x in range(rows - count, rows)})
                )

    # query
    def has_matches(self) -> bool:
        return self._combs != []

    def _get_matrix(self):
        return self._board._matrix


class BonusList(Printable):
    """
    класс анализа
    список бонусов, доступных игроку
    """

    # _bonus_list: set[Bonus]
    # _remove_bonus_status: int = -1

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

    @abstractmethod
    def get_remove_bonus_status(self) -> int:
        pass


class ConcreteBonusList(BonusList):

    def __init__(self) -> None:
        super().__init__()
        self._bonus_list: set[Bonus] = set()
        self._remove_bonus_status: int = -1

    def render(self) -> None:
        print("Bonus List: ", sep="")
        for bonus in self._bonus_list:
            print(f"{bonus}", sep=", ")
            print("\n")

    def add_bouns(self, bonus: Bonus) -> None:
        self._bonus_list.add(bonus)

    def remove_bouns(self, bonus: Bonus) -> None:
        if bonus in self._bonus_list:
            self._bonus_list.remove(bonus)
            self._remove_bonus_status: int = 1
            return
        self._remove_bonus_status: int = 0

    def has_bouns(self, bonus: Bonus) -> bool:
        return bonus in self._bonus_list

    def get_remove_bonus_status(self) -> int:
        return self._remove_bonus_status
