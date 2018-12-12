from typing import Union
import random


def read_sudoku(filename: str) -> list:
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid


def group(values: list, n: int) -> list:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    matrix = [[j - i for j in range(n)] for i in range(n)]  # Данная строка нужна для генерациии непустого списка
    index = 0
    for i in range(n):
        for j in range(n):
            matrix[i][j] = values[index]
            index += 1
    return matrix


def display(values: list) -> None:
    """Вывод Судоку """
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(values[row][col].center(width) + ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()


def get_row(values: list, pos: tuple) -> list:
    """ Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    i = int(pos[0])
    row = list(values[i])
    return row


def get_col(values: list, pos: tuple) -> list:
    """ Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    j = pos[1]
    col = []
    for i in range(len(values)):
        col.append(values[i][j])
    return col


def get_block(values: list, pos: tuple) -> list:
    """ Возвращает все значения из квадрата, в который попадает позиция pos
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    block = []
    i = pos[0]
    j = pos[1]
    if i < 3:
        for q in range(3):
            if j < 3:
                for w in range(3):
                    block.append(values[q][w])
            elif j < 6:
                for w in range(3, 6):
                    block.append(values[q][w])
            elif j < 9:
                for w in range(6, 9):
                    block.append(values[q][w])
    elif i < 6:
        for q in range(3, 6):
            if j < 3:
                for w in range(3):
                    block.append(values[q][w])
            elif j < 6:
                for w in range(3, 6):
                    block.append(values[q][w])
            elif j < 9:
                for w in range(6, 9):
                    block.append(values[q][w])
    elif i < 9:
        for q in range(6, 9):
            if j < 3:
                for w in range(3):
                    block.append(values[q][w])
            elif j < 6:
                for w in range(3, 6):
                    block.append(values[q][w])
            elif j < 9:
                for w in range(6, 9):
                    block.append(values[q][w])
    return block


def find_empty_positions(grid: list) -> tuple:
    """ Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    q = -1
    w = -1
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == '.':
                q = i
                w = j
                break
        if q >= 0 & w >= 0:
            break
    if q >= 0 & w >= 0:
        return q, w
    else:
        return -1, -1


def find_possible_values(grid: list, pos: tuple) -> list:
    """ Вернуть множество всех возможных значения для указанной позиции
    >>> grid = read_sudoku('puzzles/puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> set(values) == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> set(values) == {'2', '5', '9'}
    True
    """
    values = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    possible_values = []
    row = get_row(grid, pos)
    col = get_col(grid, pos)
    block = get_block(grid, pos)
    for i in values:
        if i in row:
            continue
        elif i in col:
            continue
        elif i in block:
            continue
        else:
            possible_values.append(i)
    return possible_values


def solve(grid: list) -> Union[list, None]:
    """ Решение пазла, заданного в grid """
    """ 
    >>> grid = read_sudoku('puzzle1.txt'    )
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', 
    '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', 
    '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', 
    '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    pos = find_empty_positions(grid)
    if pos[0] == -1:
        return grid
    i, j = pos
    possible_values = find_possible_values(grid, pos)
    for value in possible_values:
        grid[i][j] = value
        solution = solve(grid)
        if solution:
            return solution
    grid[i][j] = '.'
    return None


def check_solution(solution: list) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    check = set('123456789')
    for i in range(len(solution)):
        col = set(get_col(solution, (0, i)))
        if col != check:
            return False
    for j in range(len(solution)):
        row = set(get_row(solution, (j, 0)))
        if row != check:
            return False
    for q in range(0, 9, 3):
        for w in range(0, 9, 3):
            block = set(get_block(solution, (q, w)))
            if block != check:
                return False
    return True


def generate_sudoku(n: int) -> Union[list, None]:
    """ Генерация судоку заполненного на N элементов
    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    grid: list = []
    for i in range(9):
        grid.append(['.']*9)
    gridd = solve(grid)
    n = 81 - min(81, max(0, n))
    while n:
        i = random.randint(0, 8)
        j = random.randint(0, 8)
        if grid[i][j] != '.':
            grid[i][j] = '.'
            n -= 1
    return gridd
