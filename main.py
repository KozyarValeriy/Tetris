"""
    Скрипт с игрой тетрис.

>>> grid = set_backend((16, 18))
>>> grid[0][0]
'║'
>>> _current_figure = tetris_classes.Figure1()
>>> _current_figure.check_position((5, 1), grid)
True
>>> print_field(_current_figure.coordinate((5, 1)), grid, 0, 0, _current_figure.angle, _current_figure.symbol)
<BLANKLINE>
║              ║    Your score: 0
║    ▪         ║
║    ▪         ║
║    ▪▪        ║
║              ║
║              ║
║              ║
║              ║
║              ║
║              ║
║              ║
║              ║
║              ║
║              ║
║              ║
║              ║
║              ║
╚══════════════╝
Step is: 0
Angle: 0
"""

import subprocess
import sys
import time
import random
import copy
from pynput.keyboard import Key, Listener

import tetris_classes

# определние функции для расчета времени на основе операционной системы
time_func = time.perf_counter if sys.platform.startswith('win') else time.time

# начальные значения переменных
_grid = []
_point = None
_current_figure = None
_next_figure = None
_delay = 0.5
_step = 0
_score = 0

# константы
FIGURES = (tetris_classes.Figure1, tetris_classes.Figure2, tetris_classes.Figure3, tetris_classes.Figure4,
           tetris_classes.Figure5, tetris_classes.Figure6, tetris_classes.Figure7)

# Определение функции очистки экрана в зависимости от операционной системы
if sys.platform.startswith('win'):
    def screen_clear():
        subprocess.call(['cmd.exe', '/C', 'cls'])
else:
    def screen_clear():
        subprocess.call(['clear'])


def main(size: tuple):
    """ Функция работы тетриса

    :param size: размеры игрового поля.
    """
    global _point, _delay, _grid, _current_figure, _next_figure, _score, _step
    middle = size[0] // 2
    _grid = set_backend(size)
    screen_clear()
    listener = None
    # next_figure = None
    # step = score = 0
    try:
        listener = Listener(on_press=on_press)
        listener.start()
        while True:
            _point = (middle, 0)
            _current_figure, _next_figure = add_new_figure(_next_figure)
            current_coord = _current_figure.coordinate(_point)
            print_field(current_coord, _grid, _score, _step, _current_figure.angle, _current_figure.symbol)
            while True:
                if timer(_delay):
                    _step += 1
                    _delay = 0.5
                    # _point = (_point[0], _point[1] + 1)
                    if _current_figure.check_position((_point[0], _point[1] + 1), _grid):
                        _point = (_point[0], _point[1] + 1)
                        current_coord = _current_figure.coordinate(_point)
                        print_field(current_coord, _grid, _score, _step, _current_figure.angle, _current_figure.symbol)
                    else:
                        # _point = (_point[0], _point[1] - 1)
                        break
            current_coord = _current_figure.coordinate(_point)
            frost_figure(current_coord, _grid)
            _score = remove_layer(_grid, _score)
            if not all(el == ' ' for el in _grid[0][1:-1]):
                current_coord = _current_figure.coordinate(_point)
                print_field(current_coord, _grid, _score, _step, _current_figure.angle, _current_figure.symbol)
                print('You lose')
                break
    except KeyboardInterrupt as err:
        print(err)
    except Exception as err:
        print('ERROR')
        print(err)
        print('Point: ' + str(_point))
        print('Grid: ' + str(_grid[0]))
        time.sleep(5)
    finally:
        if listener is not None:
            listener.stop()


def set_backend(size: tuple) -> list:
    """ Функция для получения чистого игрового поля

    :param size: размеры игрового поля,
    :return: игровое поле в формате двумерного массива
    """
    grid = []
    for row in range(size[1]):
        grid.append([])
        for col in range(size[0]):
            if row < size[1] - 1:
                if col == 0 or col == size[0] - 1:
                    grid[-1].append('║')
                else:
                    grid[-1].append(' ')
            else:
                if col == 0:
                    grid[-1].append('╚')
                elif col == size[0] - 1:
                    grid[-1].append('╝')
                else:
                    grid[-1].append('═')
    return grid


def print_field(points: tuple, grid: list, score: int, step: int, angle: int, symbol: str) -> None:
    """ Функция для отрисовки игрового поля

    :param points: кортеж точек текущей фигуры,
    :param grid: текущее игровое поле,
    :param score: текущее кол-во очков игрока,
    :param step: текущий шаг в игре,
    :param angle: текущий угол фигуры,
    :param symbol: символ для отрисовки фигуры
    """
    # s = '\tYour score: {0}'.format(_score)
    plot = copy.deepcopy(grid)
    plot[0].append('    Your score: {0}'.format(score))
    plot[1].append('    Next figure:')
    # для отрисовки следующей фигуры
    figure = [[' ', ' ', ' '],
              [' ', ' ', ' '],
              [' ', ' ', ' '],
              [' ', ' ', ' ']]
    flag = False  # фалг для координат, которые меньше 0
    for x, y in _next_figure.start_point:
        figure[y][x] = _next_figure.symbol
        if x < 0:
            flag = True
    if flag:
        # если была координата меньше нуля, то нужно все элементы с конца вставить в начало
        for line in figure:
            last = line.pop(len(line) - 1)
            line.insert(0, last)
    for x, y in points:
        plot[y][x] = symbol
    screen_clear()
    print()
    for row in range(len(plot)):
        if 2 < row < 7:
            print(''.join(plot[row] + [' '] * 8 + figure[row - 3]))  # + (s if row == 0 else ''))
        else:
            print(''.join(plot[row]))
    print('Step is: {0}'.format(step))
    print('Angle: {0}'.format(angle))


def add_new_figure(next_figure: tetris_classes.Figure = None) -> tuple:
    """ Функция для получения новой фигуры

    :param next_figure: следуюущая фигура, или None, если это первый ход,
    :return: кортеж вида (новая_текущая_фигура, новая_следующая_фигура).
    """
    figure = random.choice(FIGURES)
    if next_figure is None:
        current_figure = figure()
        figure = random.choice(FIGURES)
        new_next_figure = figure()
    else:
        current_figure = next_figure
        new_next_figure = figure()
    return current_figure, new_next_figure


def on_press(key):
    """ Функция обработчик нажатий

    :param key: кнопка, которая нажата в текущий момент.
    """
    global _point, _current_figure, _delay, _score, _step
    if key == Key.right:
        if _point[0] < len(_grid[0]) - 2:
            if _current_figure.check_position((_point[0] + 1, _point[1]), _grid):
                _point = (_point[0] + 1, _point[1])
                print_field(_current_figure.coordinate(_point), _grid, _score, _step, _current_figure.angle,
                            _current_figure.symbol)
    elif key == Key.left:
        if _point[0] > 1:
            if _current_figure.check_position((_point[0] - 1, _point[1]), _grid):
                _point = (_point[0] - 1, _point[1])
                print_field(_current_figure.coordinate(_point), _grid, _score, _step, _current_figure.angle,
                            _current_figure.symbol)
    elif key == Key.up:
        _point = _current_figure.change_angle(_point, _grid)
        print_field(_current_figure.coordinate(_point), _grid, _score, _step, _current_figure.angle,
                    _current_figure.symbol)
    elif key == Key.down:
        _delay = 0.1
    elif key == Key.esc:
        print('ESC')


def timer(delay=0.5):
    """ Функция для счетчика времени

    :param delay: задержка в секундах.
    """
    try:
        # пробуем получить атрибут функции
        getattr(timer, 'time')
    except AttributeError:
        # если его нет, то добавляем атрибут и записываем в него время
        timer.time = time_func()
    if time_func() - timer.time > delay:
        timer.time = time_func()
        return True


def frost_figure(coords: tuple, grid: list, symbol='+'):
    """ Функция для заморозки фигуры при касании снизу

    :param coords: координаты фигуры,
    :param grid: игровое поле,
    :param symbol: символ, которым нужно отрисовать замороженную фигуру.
    """
    for x, y in coords:
        grid[y][x] = symbol


def remove_layer(grid: list, score: int) -> int:
    """ Функция для удаления слоя при его полном заполнении

    :param grid: игровое поле, в котором надо проверить и, при необходимости, удалить слой
    :param score: текущее кол-во очков игрока,
    :return: кол-во очков игрока после удаления слоев.
    """
    layer = len(grid) - 2
    while layer >= 0:
        if all(grid[layer][x] == '+' for x in range(1, len(grid[0]) - 1)):
            for y in range(layer, 0, -1):
                grid[y] = grid[y - 1]
            grid[0] = ['║'] + [' '] * (len(_grid[0]) - 2) + ['║']
            score += 1
            screen_clear()
        else:
            layer -= 1
    return score


if __name__ == '__main__':
    # import doctest
    # doctest.testmod()
    # time.sleep(5)
    game_size = (16, 18)
    main(game_size)
