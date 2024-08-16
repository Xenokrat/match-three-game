# Match-three CLI

Консольная версия знаменитой игры ["Три-в-ряд"](https://ru.wikipedia.org/wiki/%D0%A2%D1%80%D0%B8_%D0%B2_%D1%80%D1%8F%D0%B4)
ASCII графика.
Приложение запускается из консоли.
Отрисовывается сетка 8x8 клеток, содержащая элементы A, B, C, D, E.
Игрок вводит каждый ход координаты клеток, которые нужно поменять местами.
Поменяные местами элементы должны образовать ряд из минимум 3 элементов.
Выстроенные в ряд элементы унтичтожаются, на их место смещаются элементы сверху.
Различные комбинации элементов дают разное количество очков.

# Установка

В проекте не используются какие либо зависимости, кроме Python >= 3.11

```sh
git clone https://github.com/Xenokrat/match-three-game
cd match-three-game
python3 main.py
```

# Управление

```
q - выход из игры
[row][col],[row][col]- обменять элементы поля местами (пример валидной команды - 11,22)
```

# TODO

- Реорганизовать структуру модулей
- Реализация системы бонусов и их использования
- Реализация сохранения/загрузки, а также отмены ходов.
- Подобие анимаций для игрового процесса
- Привести в порядок тесты
