import math


class Figure:
    """ Common class for tetris figure """

    def __init__(self, angle=0, symbol='▪', coord=None):
        self.__angle = angle
        self.__symbol = symbol
        self.__start_point = coord
        self.__coord = coord

    @property
    def angle(self):
        return self.__angle

    @property
    def symbol(self):
        return self.__symbol

    @property
    def start_point(self):
        return self.__start_point

    def change_angle(self, point, grid):
        """ Method to change figure angle.
            
            Method checks the validity of rotation and returns 
            the checked point.
        """
        angle = self.__angle + 1 if self.__angle < 3 else 0
        if self.check_position(point, grid, angle=angle):
            self.__angle = angle
            self.__coord = self.rotate()
            return point
        sign_x = -1 if point[0] > len(grid[0]) // 2 else 1
        for i in range(1, 4):
            if self.check_position((point[0] + sign_x * i, point[1]), grid, angle=angle):
                self.__angle = angle
                self.__coord = self.rotate()
                return point[0] + sign_x * i, point[1]

    def check_position(self, point, grid, angle=None) -> bool:
        """ Method to check the validity of position. """
        coord = self.rotate(new_angle=angle)
        if all(grid[y][x] == ' ' for x, y in self.coordinate(point=point, coord=coord)):
            return True
        return False

    def rotate(self, new_angle=None) -> tuple:
        ans = []
        angle = (self.__angle if new_angle is None else new_angle) * math.pi / 2
        for x, y in self.__start_point:
            ans.append((round(x * math.cos(angle) - y * math.sin(angle)),
                        round(x * math.sin(angle) + y * math.cos(angle))))
        return tuple(ans)

    def coordinate(self, point, coord=None):
        """ Method for obtaining coordinates of figure. """
        ans = []
        for x, y in (self.__coord if coord is None else coord):
            ans.append((point[0] + x, point[1] + y))
        return tuple(ans)


class Figure1(Figure):
    """
    +
    +
    ++
    """

    def __init__(self, angle=0, symbol='▪'):
        start_point = ((0, 0), (0, 1), (0, 2), (1, 2))
        super().__init__(angle, symbol, start_point)


class Figure2(Figure):
    """
    +
    +
    +
    +
    """

    def __init__(self, angle=0, symbol='▪'):
        start_point = ((0, 0), (0, 1), (0, 2), (0, 3))
        super().__init__(angle, symbol, start_point)


class Figure3(Figure):
    """
     +
     +
    ++
    """

    def __init__(self, angle=0, symbol='▪'):
        start_point = ((0, 0), (0, 1), (0, 2), (-1, 2))
        super().__init__(angle, symbol, start_point)


class Figure4(Figure):
    """
     +
    +++
    """

    def __init__(self, angle=0, symbol='▪'):
        start_point = ((0, 0), (-1, 1), (0, 1), (1, 1))
        super().__init__(angle, symbol, start_point)


class Figure5(Figure):
    """
    ++
    ++
    """

    def __init__(self, angle=0, symbol='▪'):
        start_point = ((0, 0), (1, 0), (0, 1), (1, 1))
        super().__init__(angle, symbol, start_point)


class Figure6(Figure):
    """
    +
    ++
     +
    """

    def __init__(self, angle=0, symbol='▪'):
        start_point = ((0, 0), (0, 1), (1, 1), (1, 2))
        super().__init__(angle, symbol, start_point)


class Figure7(Figure):
    """
     +
    ++
    +
    """

    def __init__(self, angle=0, symbol='▪'):
        start_point = ((0, 0), (0, 1), (-1, 1), (-1, 2))
        super().__init__(angle, symbol, start_point)
