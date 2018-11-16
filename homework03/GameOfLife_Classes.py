import pygame
from pygame.locals import *
import random
from copy import deepcopy


class GameOfLife:

    def __init__(self, width: int = 640, height: int = 480,
                 cell_size: int = 10, speed: int = 10):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self):
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self):
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        self.clist = CellList(self.cell_height, self.cell_width, True)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_cell_list()
            self.clist.update()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def draw_cell_list(self):
        """
        Отображение списка клеток 'rects' с закрашиванием их в
        соответствующе цвета
        """
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                x = j * self.cell_size + 1
                y = i * self.cell_size + 1
                if self.clist.grid[i][j].is_alive():
                    pygame.draw.rect(game.screen, pygame.Color('green'),
                                     (x, y, game.cell_size - 1,
                                      game.cell_size - 1))
                else:
                    pygame.draw.rect(game.screen, pygame.Color('white'),
                                     (x, y, game.cell_size - 1,
                                      game.cell_size - 1))
        return self


class Cell:

    def __init__(self, row: int, col: int, state: bool = False):
        self.state = state
        self.row = row
        self.col = col

    def is_alive(self):
        return self.state


class CellList:

    def __init__(self, nrows: int, ncols: int, randomize: bool = False):
        self.nrows = nrows
        self.ncols = ncols
        self.grid: list = []
        for i in range(self.nrows):
            self.grid.append([])
            for j in range(self.ncols):
                if randomize:
                    self.grid[i].append(Cell(i, j, bool(random.randint(0, 1))))
                else:
                    self.grid[i].append(Cell(i, j, False))

    def get_neighbours(self, cell: Cell) -> list:
        row = cell.row
        col = cell.col
        neighbours = []
        if (row != 0) & (row != self.nrows - 1) & (col != 0) & \
                (col != self.ncols - 1):  # Клетки, не с краю
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (i == 0) & (j == 0):
                        continue
                    else:
                        neighbours.append(self.grid[row + i][col + j])
        elif (row == 0) & (col != 0) & (col != self.ncols - 1):
            # Первая строка без углов
            for i in range(0, 2):
                for j in range(-1, 2):
                    if (i == 0) & (j == 0):
                        continue
                    neighbours.append(self.grid[row + i][col + j])
        elif (row == self.nrows - 1) & (col != 0) & (col != self.ncols - 1):
            # последняя строка без углов
            for i in range(-1, 1):
                for j in range(-1, 2):
                    if (i == 0) & (j == 0):
                        continue
                    neighbours.append(self.grid[row + i][col + j])
        elif (col == 0) & (row != 0) & (row != self.nrows - 1):
            # Первая колонка без углов
            for i in range(-1, 2):
                for j in range(0, 2):
                    if (i == 0) & (j == 0):
                        continue
                    neighbours.append(self.grid[row + i][col + j])
        elif (col == self.ncols - 1) & (row != 0) & (row != self.nrows - 1):
            for i in range(-1, 2):
                for j in range(-1, 1):
                    if (i == 0) & (j == 0):
                        continue
                    neighbours.append(self.grid[row + i][col + j])
        elif (row == 0) & (col == 0):
            neighbours.append(self.grid[row][col + 1])
            neighbours.append(self.grid[row + 1][col])
            neighbours.append(self.grid[row + 1][col + 1])
        elif (row == self.nrows - 1) & (col == 0):
            neighbours.append(self.grid[row][col + 1])
            neighbours.append(self.grid[row - 1][col])
            neighbours.append(self.grid[row - 1][col + 1])
        elif (row == 0) & (col == self.ncols - 1):
            neighbours.append(self.grid[row][col - 1])
            neighbours.append(self.grid[row + 1][col])
            neighbours.append(self.grid[row + 1][col - 1])
        elif (row == self.nrows - 1) & (col == self.ncols - 1):
            neighbours.append(self.grid[row][col - 1])
            neighbours.append(self.grid[row - 1][col])
            neighbours.append(self.grid[row - 1][col - 1])
        return neighbours

    def update(self):
        new_clist = deepcopy(self.grid)
        for cell in self:
            neighbours = self.get_neighbours(cell)
            alive = sum(c.is_alive() for c in neighbours)
            if new_clist[cell.row][cell.col].is_alive():
                if alive < 2 or alive > 3:
                    new_clist[cell.row][cell.col].state = 0
            else:
                if alive == 3:
                    new_clist[cell.row][cell.col].state = 1
        self.grid = new_clist
        return self

    def __iter__(self):
        self.i_count, self.j_count = 0, 0
        return self

    def __next__(self):
        if self.i_count == self.nrows:
            raise StopIteration

        cell = self.grid[self.i_count][self.j_count]
        self.j_count += 1
        if self.j_count == self.ncols:
            self.i_count += 1
            self.j_count = 0

        return cell

    def __str__(self):
        str = ""
        for i in range(self.nrows):
            for j in range(self.ncols):
                if self.grid[i][j].state:
                    str += '1 '
                else:
                    str += '0 '
            str += '\n'
        return str

    @classmethod
    def from_file(cls, filename: str):
        grid = []
        with open(filename) as f:
            for i, line in enumerate(f):
                grid.append([Cell(i, j,
                                  bool(int(c))) for j, c in enumerate(line)
                             if c in '01'])
        celllist = cls(len(grid), len(grid[0]), False)
        celllist.grid = grid
        return celllist


if __name__ == '__main__':
    game = GameOfLife(360, 360, 40)
    game.run()
