"""
>>> set_backend((16, 18))
>>> _grid[0][0]
'║'
>>> _current_figure = TetrisClass.Figure_1()
>>> _current_figure.check_position((5, 1), _grid)
True
>>> print_field(_current_figure.coordinate((5, 1)))
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
>>> _grid = []
>>> print(_grid)
[]
"""

import subprocess
import sys
import time
import random
import copy
from threading import Thread
from pynput.keyboard import Key, Listener

import TetrisClass

time_func = time.perf_counter if sys.platform.startswith('win') else time.time

_start_time = time_func()
_grid = []
_current_figure = None
_next_figure = None
_point = (0, 0)
_score = 0
_delay = 0.5
_step = 0
FIGURES = [TetrisClass.Figure1, TetrisClass.Figure2, TetrisClass.Figure3, TetrisClass.Figure4,
           TetrisClass.Figure5, TetrisClass.Figure6, TetrisClass.Figure7]


def main(size):
    global _point, _delay, _step
    middle = size[0] // 2
    set_backend(size)
    screen_clear()
    try:
        lis = Listener(on_press=on_press)
        lis.start()
        while True:
            _point = (middle, 0)
            add_new_figure()
            print_field(_current_figure.coordinate(_point))
            while True:
                if timer(_delay):
                    _step += 1
                    _delay = 0.5
                    # _point = (_point[0], _point[1] + 1)
                    if _current_figure.check_position((_point[0], _point[1] + 1), _grid):
                        _point = (_point[0], _point[1] + 1)
                        print_field(_current_figure.coordinate(_point))
                    else:
                        # _point = (_point[0], _point[1] - 1)
                        break
            frost_figure(_current_figure.coordinate(_point))
            remove_layer()
            if not all(el == ' ' for el in _grid[0][1:-1]):
                print_field(_current_figure.coordinate(_point))
                print('You lose')
                lis.stop()
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
        lis.stop()


if sys.platform.startswith('win'):
    def screen_clear():
        subprocess.call(['cmd.exe', '/C', 'cls'])
else:
    def screen_clear():
        subprocess.call(['clear'])


def set_backend(size):
    """ Function to preset the playing field. """
    global _grid
    _grid = []
    for row in range(size[1]):
        _grid.append([])
        for col in range(size[0]):
            if row < size[1] - 1:
                if col == 0 or col == size[0] - 1:
                    _grid[-1].append('║')
                else:
                    _grid[-1].append(' ')
            else:
                if col == 0:
                    _grid[-1].append('╚')
                elif col == size[0] - 1:
                    _grid[-1].append('╝')
                else:
                    _grid[-1].append('═')


def print_field(points):
    """ Function to print the playing field. """
    # s = '\tYour score: {0}'.format(_score)
    plot = copy.deepcopy(_grid)
    plot[0].append('    Your score: {0}'.format(_score))
    # plot[1].append('    Next figure:')
    # figure = [[[], []],
    #           [[], []],
    #           [[], []],
    #           [[], []]]
    # for x, y in _next_figure.start_point:
    #     if y >= len(figure):
    #         figure.append([])
    #     figure[y].append(_next_figure.symbol)
    for x, y in points:
        plot[y][x] = _current_figure.symbol
    screen_clear()
    for row in range(len(_grid)):
        print(''.join(plot[row]))  # + (s if row == 0 else ''))
    print('Step is: {0}'.format(_step))
    print('Angle: {0}'.format(_current_figure.angle))


def add_new_figure():
    """ Function to select a new figure. """
    global _current_figure, _next_figure
    number = random.choice([0, 1, 2, 3, 4, 5, 6])
    if _current_figure is None:
        _current_figure = FIGURES[number]()
        number = random.choice([0, 1, 2, 3, 4, 5, 6])
        _next_figure = FIGURES[number]()
    else:
        _current_figure = _next_figure
        _next_figure = FIGURES[number]()



def on_press(key):
    """ Function to handle a click event. """
    global _point, _current_figure, _delay
    if key == Key.right:
        if _point[0] < len(_grid[0]) - 2:
            if _current_figure.check_position((_point[0] + 1, _point[1]), _grid):
                _point = (_point[0] + 1, _point[1])
                # print_field(_curren_figure.coordinate(_point))
    elif key == Key.left:
        if _point[0] > 1:
            if _current_figure.check_position((_point[0] - 1, _point[1]), _grid):
                _point = (_point[0] - 1, _point[1])
                # print_field(_curren_figure.coordinate(_point))
    elif key == Key.up:
        _point = _current_figure.change_angle(_point, _grid)
    elif key == Key.down:
        _delay = 0.1
    elif key == Key.esc:
        return False


def timer(delay=0.5):
    """ Counter. """
    global _start_time
    if time_func() - _start_time > delay:
        _start_time = time_func()
        return True


def frost_figure(coords, symbol='+'):
    """ Function to set figure on the playing field at the end of the turn. """
    global _grid
    for x, y in coords:
        _grid[y][x] = symbol


def remove_layer():
    """ Function to remove a filled layer. """
    global _score, _grid
    layer = len(_grid) - 2
    while layer >= 0:
        if all(_grid[layer][x] == '+' for x in range(1, len(_grid[0]) - 1)):
            for y in range(layer, 0, -1):
                _grid[y] = _grid[y - 1]
            _grid[0] = ['║'] + [' '] * (len(_grid[0]) - 2) + ['║']
            _score += 1
            screen_clear()
        else:
            layer -= 1


if __name__ == '__main__':
    # import doctest
    # doctest.testmod()
    # time.sleep(5)
    size = (16, 18)
    main(size)
