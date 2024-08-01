"""
Учет событий, происходящих в течении игры
(ходы, подсчёт очков)
"""

from .utils import _CommandStatus


class UserCommand(ABC):
    """
    Отвечает за управление пользователем игрой
    через интерфейс
    - Ввод ходов
    - Конце игры
    - Начать заново
    - Отмотать до x хода
    - Активировать бонус
    """

    # constructor
    def __init__(self) -> None:
        self._apply_command_status = _CommandStatus.NIL

    # commands
    def apply_command(self) -> None:
        """
        pre: состояние игры позволяет применить команду
        post: состояние игры изменено по команде
        """

    # queries
    def get_apply_command_status(self) -> _CommandStatus:
        return self._apply_command_status


class Score(ABC):
    """
    Отвечает за подсчёт очков для игрока
    в ходе игры.
    """

    # constructor
    def __init__(self) -> None:
        self._score: int = 0

        self._remove_score_status = _CommandStatus.NIL

    # commands
    def add_score(self, score_add: int) -> None:
        """
        pre: 
        post: значение очков добавлено
        """

    def remove_score(self, score_minus: int) -> None:
        """
        pre:  значение очков достаточно
        post: значение очков убрано
        """

    # queries
    def get_score(self) -> int:
        return self._score

    def get_remove_score_status(self) -> _CommandStatus.NIL:
        return self._remove_score_status


class BonusList(ABC):
    """
    Реализует хранение имеющихся у игрока бонусов
        думаю, словарь "bouns: кол-во" 
    """

    # constructor
    def __init__(self) -> None:
        self._bonus_list: list[Bonus] = []

        self._bonus_remove_status = _CommandStatus.NIL

    # commands
    @abstractmethod
    def add_bonus(self) -> None:
        """
        pre: 
        post: новый бонус включён в список
        """

    @abstractmethod
    def remove_bonus(self) -> None:
        """
        pre:  бонус есть
        post: бонус удалён из списка
        """

    @abstractmethod
    def apply_bonus(self) -> None:
        """
        pre:  бонус есть
        post: бонус удалён из списка, его эффект применён на матрицу
        """

    # queries
    def show_bonus_list(self) -> list[Bonus]:
        return self._bonus_list

    def get_bonus_remove_status(self) -> _CommandStatus:
        return self._bonus_remove_status


class History(ABC):
    """
    Реализует хранение ходов игры, как состояния поля
        по идее будет хорош стек, т.к. он даст нам Undo хода
        если добавить второй стек, это даст нам операцию Redo
    """

    # constructor
    def __init__(self) -> None:
        self._history_list: list[tuple[Matrix, Score, BonusList]] = []

        self._undo_status = _CommandStatus.NIL

    # commands
    def undo(self) -> None:
        """
        pre: ход больше первого
        post: состояние игры возвращено на предыдущий ход, учитывая поле, счёт и бонусы
        """
        ...

    def update(self) -> None:
        """
        pre: 
        post: добавлено состояние игры после хода или бонуса
        """
        ...

    # queries
    def show_move_count(self) -> int:
        ...

    def get_undo_status(self) -> _CommandStatus:
        return self._undo_status


