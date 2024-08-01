"""
Вывод в консоль отображения
элементов игры и интерфейс пользователя
"""

from abc import ABC

from .utils import _CommandStatus


# Widgets
class AdtWidget(ABC):
    """
    Отображениe в консоль элемента игры
    """


class Widget(AdtWidget):
    """
    Отображениe в консоль всех игровых элементов
    """

    # constructor
    def __init__(self) -> None:
        self._is_shown = True
        self._template = ""

    # commands
    @abstractmethod
    def print_to_ui(self, info: str) -> None
        """
        pre:
        post: отображение выведено в консоль
        """

    @abstractmethod
    def hide(self) -> None
        """
        pre:
        post: статус изменен на _is_shown = False
        """


class UiCommandLine(Widget):
    """
    Отвечает за отображение интерфейса ввода комманд пользователем
    для управления игрой
    """

    def __init__(self) -> None:
        super().__init__()
        self._template = "" # TODO:


class UiMatrix(Widget):
    """
    Отвечает за вывод текущего состояния игры в консоль
    """

    def __init__(self) -> None:
        super().__init__()
        self._template = "" # TODO:


class UiStats(Widget):
    """
    Ввыод на экран
    Очков пользователя
    Текущий ход (номер)
    """

    def __init__(self) -> None:
        super().__init__()
        self._template = "" # TODO:


class UiBonus(Widget):
    """
    Ввыод на экран
    Доступных для активации бонусов
    """

    def __init__(self) -> None:
        super().__init__()
        self._template = "" # TODO:


class UiCommands(Widget):
    """
    Ввыод на экран
    Доступных действий для пользователя
    """

    def __init__(self) -> None:
        super().__init__()
        self._template = "" # TODO:


class UserInterface(AdtUserInterface):

    # constructor
    def __init__(self) -> None:
        super().__init__()
        self._widgets: Widget = []

    # command
    def add_widget(self, widget: Widget) -> None:
        """
        pre: 
        post: добавлен виджет
        """
        self._widgets.append(widget)

    def remove_widget(self, widget: Widget) -> None:
        """
        pre:  
        post: добавлен виджет
        """
        self._widgets.append(widget)

    # queries
    def show_widgets(self) -> None:
        # TODO:
        ...
