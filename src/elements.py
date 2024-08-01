"""
Объекты, состовляющие игровое поле
и участвующие в процессе игры
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Self, override

from .utils import _CommandStatus


# Types
Coords = tuple[
    tuple[int, int], 
    tuple[int, int]
]


# Elements
class AdtElement(ABC):
    """
    Элемент конкретного типа, который занимает
    клетку поля (A, B, C, D, E)
    """


class _ElemntEnum(Enum):
    EMPTY = 0
    A = 1
    B = 2
    C = 3
    D = 4
    E = 5


class Element(AdtElement):

    # constructor
    def __init__(self) -> None:
        self._element = _ElemntEnum.EMPTY

    # commands
    @abstractmethod
    def set_type(self, elem_type: _ElemntEnum) -> None:
        """
        pre:
        post: установлен тип Element, отличный от EMPTY
        """
        # TODO:

    @abstractmethod
    def delete_type(self) -> None:
        """
        pre:
        post: установлен тип Element == EMPTY
        """
        # TODO:

    # queries
    def get_type(self) -> _ElemntEnum:
        """Возвращает тип элемента"""
        return self._element

    @override
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Self):
            return self._element == other._get_type()
        return False


# Matrix
class AdtMatrix(ABC):
    """
    Реализует хранение текущего состояния игры
        двумерный массив
    """


class _MatrixState(Enum):
    DEFAULT = 0
    DELETE_ELEMS = 1
    SHIFT_ELEMS = 2
    ADD_ELEMS = 3


class Matrix(AdtMatrix):

    # constructor
    def __init__(self, size: tuple[int, int]) -> None:
        self._matrix: list[list[AdtElement]] = [[Element()] * size[1]] * size[0]
        self._state = _MatrixState.DEFAULT

        self._change_element_status = _CommandStatus.NIL

    # commands
    @abstractmethod
    def set_state(self, new_state: _MatrixState) -> None:
        """
        pre:
        post: установлено состояние new_state
        """

    @abstractmethod
    def change_element(self, coords: Coords, elem_status: _ElemntEnum) -> None:
        """
        pre:  координаты в пределах поля
        post: состояние элемента в coords == EMPTY
        """

    # queries
    @abstractmethod
    def has_moves(self) -> bool:
        pass

    def get_state(self) -> _MatrixState:
        return self._state



class Event(ABC):
    """
    Алгоритм обработки события, которое приводит к изменению игрового поля
    """

    # constructor
    def __init__(self, matrix: AdtMatrix) -> None:
        self._matrix = matrix
        self._event_log = []

        self._resolve_state_status = _CommandStatus.NIL

    # commands
    @abstractmethod
    def resolve_state(self) -> None:
        """
        pre:  стейт установлен на DEFAULT
        post: стейт установлен на DEFAULT
        """

    @abstractmethod
    def _delete_elements(self) -> None:
        """
        pre:  state == DELETE_ELEMS
        post: элементы, давшие комбинации, становятся пустыми
        post: обновлен лог какие элементы были "уничтожены"
        post: стейт установлен на SHIFT_ELEMS
        """

    @abstractmethod
    def _shift_elements(self) -> None:
        """
        pre:  state == SHIFT_ELEMS
        post: не-пустые элементы смещены вниз на место пустых
        post: стейт установлен на ADD_ELEMS
        """

    @abstractmethod
    def _add_new_elements(self) -> None:
        """
        pre:  state == ADD_ELEMS
        post: пустые элементы заменены на новые
        post: стейт установлен на DELETE_ELEMS или DEFAULT
        """

    # queries
    def get_resolve_state_status(self) -> _CommandStatus:
        return self._resolve_state_status


class MoveEvent(Event):

    # constructor
    def __init__(self, matrix: AdtMatrix) -> None:
        super().__init__(matrix)
        self._accept_move_status = _CommandStatus.NIL

    # commands
    @abstractmethod
    def accept_move(self, coords: Coords) -> None:
        """
        pre:  ход валиден
        post: элементы поменяны местами.
        post: стейт изменен на DELETE_ELEMS
        """

    # queries
    def get_accept_move_status(self) -> _CommandStatus:
        return self._accept_move_status


class BonusEvent(Event):

    # constructor
    def __init__(self, matrix: AdtMatrix) -> None:
        super().__init__(matrix)
        self._accept_bonus_status = _CommandStatus.NIL

    # commands
    @abstractmethod
    def accept_bonus(self, bonus: Bonus) -> None: # FIX:
        """
        pre:  применение бонуса возможно
        post: поле изменено согласно эффекту бонуса
        post: стейт изменен на DELETE_ELEMS
        """

    # queries
    def get_accept_bonus_status(self) -> _CommandStatus:
        return self._accept_bonus_status



