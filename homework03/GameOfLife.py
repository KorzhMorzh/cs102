import pygame
import random
from pygame.locals import *


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
        # http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        running = True
        self.clist = self.cell_list(randomize=True)
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_cell_list(self.clist)
            self.update_cell_list(self.clist)
            self.draw_grid()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def cell_list(self, randomize: bool = True) -> list:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1.
        В противном случае клетка считается мертвой, то
        есть ее значение равно 0.
        Если параметр randomize = True, то создается список, где
        каждая клетка может быть равновероятно живой или мертвой.
        """
        self.clist = []
        for i in range(self.cell_height):
            self.clist.append([])
            for j in range(self.cell_width):
                if randomize:
                    self.clist[i].append(random.randint(0, 1))
                else:
                    self.clist[i].append(0)
        return self.clist

    def draw_cell_list(self, rects: list) -> list:
        """
        Отображение списка клеток 'rects' с закрашиванием их в
        соответствующе цвета
        """
        y = 0
        for i in rects:
            x = 0
            for j in i:
                if j:
                    j = pygame.draw.rect(self.screen,
                                         pygame.Color('green'),
                                         (x, y, self.cell_size - 1,
                                          self.cell_size - 1))
                else:
                    j = pygame.draw.rect(self.screen,
                                         pygame.Color('white'),
                                         (x, y, self.cell_size - 1,
                                          self.cell_size - 1))
                x += self.cell_size
            y += self.cell_size
        return rects

    def get_neighbours(self, cell: tuple) -> list:
        """
        Вернуть список соседних клеток для клетки cell.
        Соседними считаются клетки по горизонтали,
        вертикали и диагоналям, то есть во всех
        направлениях.
        """
        row, col = cell
        neighbours = []
        if (row != 0) & (row != self.cell_height - 1) & (col != 0) \
                & (col != self.cell_width - 1):  # Клетки, не с краю
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (i == 0) & (j == 0):
                        continue
                    else:
                        neighbours.append(self.clist[row + i][col + j])
        elif (row == 0) & (col != 0) & (col != self.cell_width - 1):
            # Первая строка без углов
            for i in range(0, 2):
                for j in range(-1, 2):
                    if (i == 0) & (j == 0):
                        continue
                    neighbours.append(self.clist[row + i][col + j])
        elif (row == self.cell_height - 1) & (col != 0) & \
                (col != self.cell_width - 1):  # последняя строка без углов
            for i in range(-1, 1):
                for j in range(-1, 2):
                    if (i == 0) & (j == 0):
                        continue
                    neighbours.append(self.clist[row + i][col + j])
        elif (col == 0) & (row != 0) & (row != self.cell_height - 1):
            # Первая колонка без углов
            for i in range(-1, 2):
                for j in range(0, 2):
                    if (i == 0) & (j == 0):
                        continue
                    neighbours.append(self.clist[row + i][col + j])
        elif (col == self.cell_width - 1) & (row != 0) \
                & (row != self.cell_height - 1):
            for i in range(-1, 2):
                for j in range(-1, 1):
                    if (i == 0) & (j == 0):
                        continue
                    neighbours.append(self.clist[row + i][col + j])
        elif (row == 0) & (col == 0):
            neighbours.append(self.clist[row][col + 1])
            neighbours.append(self.clist[row + 1][col])
            neighbours.append(self.clist[row + 1][col + 1])
        elif (row == self.cell_height - 1) & (col == 0):
            neighbours.append(self.clist[row][col + 1])
            neighbours.append(self.clist[row - 1][col])
            neighbours.append(self.clist[row - 1][col + 1])
        elif (row == 0) & (col == self.cell_width - 1):
            neighbours.append(self.clist[row][col - 1])
            neighbours.append(self.clist[row + 1][col])
            neighbours.append(self.clist[row + 1][col - 1])
        elif (row == self.cell_height - 1) & (col == self.cell_width - 1):
            neighbours.append(self.clist[row][col - 1])
            neighbours.append(self.clist[row - 1][col])
            neighbours.append(self.clist[row - 1][col - 1])
        return neighbours

    def update_cell_list(self, cell_list: list) -> list:
        """
        Обновление состояния клеток
        """
        row = 0
        col = 0
        new_clist: list = []
        for y, i in enumerate(cell_list):
            new_clist.append([])
            for x, j in enumerate(i):
                alive = 0
                dead = 0
                cell = (y, x)
                neighbours = self.get_neighbours(cell)
                col += 1
                for n in neighbours:
                    if n:
                        alive += 1
                    else:
                        dead += 1
                if j:
                    if alive < 2 or alive > 3:
                        new_clist[y].append(0)
                    else:
                        new_clist[y].append(1)
                if not j:
                    if alive == 3:
                        new_clist[y].append(1)
                    else:
                        new_clist[y].append(0)
            row += 1
            col = 0
        self.clist = new_clist
        return self.clist


if __name__ == '__main__':
    game = GameOfLife(400, 400, 10)
    game.run()
