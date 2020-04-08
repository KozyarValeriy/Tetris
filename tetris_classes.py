"""
    Скрип с классами фигу для тетриса.
"""

import math


class Figure:
    """ Общий класс для всех фигур """

    def __init__(self, max_angle: int = 3, symbol: str = '▪', coord: tuple = None):
        """ Метод инициализации объекта фигуры

        :param max_angle: максимальный угол поворота фигуры,
        :param symbol: символ для отрисовки фигуры на игровом поле,
        :param coord: координаты фигуры в поле размером 2х4.
        """
        self._angle = 0
        self._max_angle = max_angle if 0 <= max_angle < 3 else 3
        self._symbol = symbol
        self._start_coord = coord

    @property
    def max_angle(self):
        return self._max_angle

    @max_angle.setter
    def max_angle(self, new_max_angle):
        if new_max_angle > 3:
            self._max_angle = 3
        elif new_max_angle < 0:
            self._max_angle = 0
        else:
            self._max_angle = new_max_angle

    @property
    def angle(self) -> int:
        """ Свойство для получения текущего угла фигуры """
        return self._angle

    @property
    def symbol(self) -> str:
        """ Свойство для получения символа отрисовки фигуры """
        return self._symbol

    @property
    def start_point(self) -> tuple:
        """ Свойство для получения начального положения фигуры при угле поворота 0 """
        return self._start_coord

    def change_angle(self, point: tuple, grid: list) -> tuple:
        """ Метод для изменения угла положения фигуры
            
        :param point: начальная точка фигуры на поле,
        :param grid: поле, где распологаются фигуры,
        :return: допустимая точка на поле
        """
        angle = self._angle + 1 if self._angle < self._max_angle else 0
        if self.check_position(point, grid, angle=angle):
            self._angle = angle
            # self._coord = self.rotate()
            return point
        sign_x = -1 if point[0] > len(grid[0]) // 2 else 1
        # пробуем сместить фигуру, чтобы найти доступное положение
        for i in range(1, 4):
            if self.check_position((point[0] + sign_x * i, point[1]), grid, angle=angle):
                self._angle = angle
                # self._coord = self.rotate()
                return point[0] + sign_x * i, point[1]
        return point

    def check_position(self, point: tuple, grid: list, angle: int = None) -> bool:
        """ Метод для проверки правильности расположения фигуры на поле

        :param point: точка, обозначающая текущее положение фигуры на поле,
        :param grid: игровое поле,
        :param angle: текущий угол поворота фигуры
        :return: True, если позиция для фигуры допустима, иначе False
        """
        coord = self.rotate(new_angle=angle)
        if all(grid[y][x] == ' ' for x, y in self.coordinate(point=point, coord=coord)):
            # если все точки на поле в этом месте пустые, значит позиция допустима
            return True
        return False

    def rotate(self, new_angle: int = None) -> tuple:
        """ Метод для получения координат повернутой фигуры

        :param new_angle: угол, на который требуется повернуть фигуру,
        :return: координаты повернутой фигуры.
        """
        ans = []
        angle = (self._angle if new_angle is None else new_angle) * math.pi / 2
        for x, y in self._start_coord:
            ans.append((round(x * math.cos(angle) - y * math.sin(angle)),
                        round(x * math.sin(angle) + y * math.cos(angle))))
        return tuple(ans)

    def coordinate(self, point: tuple, coord: tuple = None) -> tuple:
        """ Методя для получения координат фигуры от текущей точки

        :param point: точка, относительно которой получить координаты фигуры,
        :param coord: координаты фигуры для получения (не обязательный параметр),
        :return: координаты фигуры относительно заданной точки.
        """
        ans = []
        coord = self.rotate() if coord is None else coord
        for x, y in coord:
            ans.append((point[0] + x, point[1] + y))
        return tuple(ans)


class Figure1(Figure):
    """
    +
    +
    ++
    """

    def __init__(self, symbol='▪'):
        start_point = ((0, 0), (0, 1), (0, 2), (1, 2))
        super().__init__(max_angle=3, symbol=symbol, coord=start_point)


class Figure2(Figure):
    """
    +
    +
    +
    +
    """

    def __init__(self, symbol='▪'):
        start_point = ((0, 0), (0, 1), (0, 2), (0, 3))
        super().__init__(max_angle=1, symbol=symbol, coord=start_point)


class Figure3(Figure):
    """
     +
     +
    ++
    """

    def __init__(self, symbol='▪'):
        start_point = ((0, 0), (0, 1), (0, 2), (-1, 2))
        super().__init__(max_angle=3, symbol=symbol, coord=start_point)


class Figure4(Figure):
    """
     +
    +++
    """

    def __init__(self, symbol='▪'):
        start_point = ((0, 0), (-1, 1), (0, 1), (1, 1))
        super().__init__(max_angle=3, symbol=symbol, coord=start_point)


class Figure5(Figure):
    """
    ++
    ++
    """

    def __init__(self, symbol='▪'):
        start_point = ((0, 0), (1, 0), (0, 1), (1, 1))
        super().__init__(max_angle=0, symbol=symbol, coord=start_point)


class Figure6(Figure):
    """
    +
    ++
     +
    """

    def __init__(self, symbol='▪'):
        start_point = ((0, 0), (0, 1), (1, 1), (1, 2))
        super().__init__(max_angle=1, symbol=symbol, coord=start_point)


class Figure7(Figure):
    """
     +
    ++
    +
    """

    def __init__(self, symbol='▪'):
        start_point = ((0, 0), (0, 1), (-1, 1), (-1, 2))
        super().__init__(max_angle=1, symbol=symbol, coord=start_point)
